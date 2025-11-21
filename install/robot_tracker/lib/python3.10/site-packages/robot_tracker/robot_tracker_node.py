#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, ReliabilityPolicy

import numpy as np
import math
import time
from collections import deque

from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry  # 使用 Odometry 代替 Target
from tf2_ros import Buffer, TransformListener, LookupException, ExtrapolationException
import tf2_geometry_msgs

# 暂时注释掉 robot_interfaces 的导入
from robot_interfaces.msg import Target
from robot_interfaces.action import Collect


class KalmanFilter:
    """简单的卡尔曼滤波器"""
    def __init__(self, q=0.1, r=0.1):
        # 状态向量: [x, y, vx, vy]
        self.state = np.zeros(4)
        
        # 状态协方差矩阵
        self.P = np.eye(4)
        
        # 过程噪声协方差
        self.Q = np.eye(4) * q
        
        # 观测噪声协方差
        self.R = np.eye(2) * r
        
        # 状态转移矩阵 (匀速模型)
        self.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # 观测矩阵 (只能观测位置)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
    
    def predict(self):
        """预测步骤（已弃用）：保留兼容性，使用默认 dt=1.0 调用新的 predict(dt)"""
        return self.predict_dt(1.0)

    def predict_dt(self, dt: float):
        """预测步骤，使用时间间隔 dt 来更新状态转移矩阵"""
        # 更新状态转移矩阵以反映真实时间步长
        self.F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        # 根据 dt 简单缩放过程噪声（使 Q 随时间增长），避免固定步长导致速度估计不稳定
        if dt <= 0:
            dt = 0.0
        self.state = self.F @ self.state
        # 简单地按 dt 缩放 Q（可根据需要替换为更精确的连续时间积分形式）
        self.P = self.F @ self.P @ self.F.T + (self.Q * max(dt, 1e-6))
        return self.state[:2]  # 返回预测的位置
    
    def update(self, measurement):
        """更新步骤"""
        # 计算卡尔曼增益
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # 更新状态
        y = measurement - self.H @ self.state
        self.state = self.state + K @ y
        
        # 更新协方差
        I = np.eye(4)
        self.P = (I - K @ self.H) @ self.P
        
        return self.state


class AlphaBetaFilter:
    """Alpha-Beta滤波器 (简化版卡尔曼)"""
    def __init__(self, alpha=0.5, beta=0.1):
        self.alpha = alpha
        self.beta = beta
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.last_time = None
    
    def update(self, x, y, current_time):
        """更新滤波器"""
        if self.last_time is None:
            self.x = x
            self.y = y
            self.last_time = current_time
            return self.x, self.y, self.vx, self.vy
        
        # 计算时间间隔
        dt = (current_time - self.last_time).nanoseconds / 1e9
        if dt <= 0:
            return self.x, self.y, self.vx, self.vy
        
        # 预测
        x_pred = self.x + self.vx * dt
        y_pred = self.y + self.vy * dt
        
        # 计算残差
        residual_x = x - x_pred
        residual_y = y - y_pred
        
        # 更新位置
        self.x = x_pred + self.alpha * residual_x
        self.y = y_pred + self.alpha * residual_y
        
        # 更新速度
        self.vx = self.vx + (self.beta / dt) * residual_x
        self.vy = self.vy + (self.beta / dt) * residual_y
        
        self.last_time = current_time
        return self.x, self.y, self.vx, self.vy


class RobotTrackerNode(Node):
    def __init__(self):
        super().__init__('robot_tracker')
        
        # 声明参数
        self.declare_parameter('filter_type', 'kalman')
        self.declare_parameter('process_noise', 0.01)
        self.declare_parameter('measurement_noise', 0.1)
        self.declare_parameter('kalman_q', 0.1)
        self.declare_parameter('kalman_r', 0.1)
        self.declare_parameter('alpha', 0.5)
        self.declare_parameter('beta', 0.1)
        self.declare_parameter('velocity_threshold', 0.05)
        self.declare_parameter('stationary_time', 5.0)
        self.declare_parameter('publish_frequency', 50.0)
        self.declare_parameter('target_frame', 'world')
        self.declare_parameter('action_timeout', 10.0)
        # TF 警告限频，避免大量日志刷屏
        self._last_tf_warn_time = 0.0
        
        # 获取参数
        filter_type = self.get_parameter('filter_type').value
        process_noise = self.get_parameter('process_noise').value
        measurement_noise = self.get_parameter('measurement_noise').value
        kalman_q = self.get_parameter('kalman_q').value
        kalman_r = self.get_parameter('kalman_r').value
        alpha = self.get_parameter('alpha').value
        beta = self.get_parameter('beta').value
        self.velocity_threshold = self.get_parameter('velocity_threshold').value
        self.stationary_time = self.get_parameter('stationary_time').value
        publish_frequency = self.get_parameter('publish_frequency').value
        self.target_frame = self.get_parameter('target_frame').value
        action_timeout = self.get_parameter('action_timeout').value
        
        self.get_logger().info(f"启动目标跟踪器，滤波器类型: {filter_type}")
        
        # 初始化滤波器
        if filter_type == 'kalman':
            self.filter = KalmanFilter(q=kalman_q, r=kalman_r)
        else:
            self.filter = AlphaBetaFilter(alpha=alpha, beta=beta)
        
        # TF缓冲区
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # 静止状态检测
        self.stationary_start_time = None
        self.last_velocity = 0.0
        
        # 创建发布者 - 使用 Odometry 代替 Target
        qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE
        )
        self.target_publisher = self.create_publisher(
            Odometry,  # 使用 Odometry 消息
            'robot_tracker/target', 
            qos_profile
        )
        
        # 暂时注释掉动作客户端
        self.collect_action_client = ActionClient(
            self, 
            Collect, 
            'robot_controller/collect'
        )
        
        # 创建订阅者
        self.observation_subscriber = self.create_subscription(
            PointStamped,
            'robot_sensor/observed',
            self.observation_callback,
            qos_profile
        )
        
        # 创建定时器用于定期发布
        self.publish_timer = self.create_timer(1.0/publish_frequency, self.publish_timer_callback)
        
        # 存储最新的目标状态
        self.current_target = None

        # 上一次观测时间（秒），用于计算 dt
        self.last_time = None
        
        self.get_logger().info("目标跟踪器初始化完成")
        self.get_logger().info("注意：当前使用 Odometry 消息，等 robot_interfaces 修复后将切换回 Target")
    
    def observation_callback(self, msg):
        """观测数据回调函数"""
        try:
            # 将观测数据转换到目标坐标系
            transformed_point = self.transform_point(msg, self.target_frame)
            if transformed_point is None:
                return
            
            x = transformed_point.point.x
            y = transformed_point.point.y

            # 使用观测消息的时间戳（如果可用）作为当前时间
            try:
                stamp = transformed_point.header.stamp
                msg_time = float(stamp.sec) + float(stamp.nanosec) / 1e9
            except Exception:
                # 回退到节点时钟
                msg_time = float(self.get_clock().now().nanoseconds) / 1e9

            # 计算 dt（秒）
            dt = None
            if self.last_time is not None:
                dt = msg_time - self.last_time

            # 更新滤波器
            if isinstance(self.filter, KalmanFilter):
                measurement = np.array([x, y])
                # 仅在有有效 dt 时调用 predict，否则跳过预测（首次观测）
                try:
                    if dt is not None and dt > 1e-6:
                        self.filter.predict_dt(dt)
                    # 如果没有有效 dt（首次观测），不进行预测，直接用 update 初始化状态
                except Exception:
                    pass
                state = self.filter.update(measurement)
                filtered_x, filtered_y = state[0], state[1]
                vx, vy = state[2], state[3]
            else:
                # Alpha-Beta滤波
                # AlphaBeta 期待 rclpy Time 对象，构造一个临时 Time
                try:
                    rt = rclpy.time.Time(seconds=int(msg_time), nanoseconds=int((msg_time - int(msg_time)) * 1e9))
                except Exception:
                    rt = self.get_clock().now()
                filtered_x, filtered_y, vx, vy = self.filter.update(x, y, rt)
            
            # 计算速度大小
            velocity = math.sqrt(vx**2 + vy**2)
            
            # 创建 Odometry 消息代替 Target
            odom_msg = Odometry()
            # 使用观测时间作为 header.stamp（如果可用）
            try:
                rt = rclpy.time.Time(seconds=int(msg_time), nanoseconds=int((msg_time - int(msg_time)) * 1e9))
                odom_msg.header.stamp = rt.to_msg()
            except Exception:
                odom_msg.header.stamp = self.get_clock().now().to_msg()
            odom_msg.header.frame_id = self.target_frame
            odom_msg.child_frame_id = "target"
            
            # 设置位置
            odom_msg.pose.pose.position.x = float(filtered_x)
            odom_msg.pose.pose.position.y = float(filtered_y)
            odom_msg.pose.pose.position.z = 0.0
            odom_msg.pose.pose.orientation.w = 1.0  # 无旋转
            
            # 设置速度
            odom_msg.twist.twist.linear.x = float(vx)
            odom_msg.twist.twist.linear.y = float(vy)
            odom_msg.twist.twist.linear.z = 0.0
            
            self.current_target = odom_msg
            
            # 检测静止状态，传入秒数（float）
            self.detect_stationary_state(velocity, msg_time)

            # 更新 last_time
            self.last_time = msg_time
            
        except Exception as e:
            self.get_logger().error(f"处理观测数据时出错: {e}")
    
    def transform_point(self, point, target_frame):
        """将点转换到目标坐标系

        优先使用消息时间戳进行查询；若发生 Extrapolation（请求未来时间的变换），
        则退回到使用最新时间的变换并重试一次。将 Lookup/Extrapolation 异常处理为
        debug 级别以避免过多重复 warn 日志。
        """
        # 构造要查询的时间并尝试按消息时间进行变换查询
        try:
            stamp = point.header.stamp
            tf_time = rclpy.time.Time(seconds=stamp.sec, nanoseconds=stamp.nanosec)
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                point.header.frame_id,
                tf_time
            )
            transformed_point = tf2_geometry_msgs.do_transform_point(point, transform)
            return transformed_point

        except ExtrapolationException as e:
            # 请求的是未来时间，尝试使用最新时间的变换重试一次（限频警告）
            now_sec = self.get_clock().now().nanoseconds / 1e9
            if now_sec - self._last_tf_warn_time > 1.0:
                self.get_logger().warn(f"坐标变换时间超前，尝试使用最新 TF（回退）: {e}")
                self._last_tf_warn_time = now_sec
            # 先尝试使用比消息时间早一点的时间戳（回退 10ms），以应对微小时间差
            try:
                stamp = point.header.stamp
                adj_nsec = stamp.nanosec - 10_000_000
                adj_sec = stamp.sec
                if adj_nsec < 0:
                    adj_sec = stamp.sec - 1
                    adj_nsec = max(0, stamp.nanosec + 1_000_000_000 - 10_000_000)
                tf_time_adj = rclpy.time.Time(seconds=int(adj_sec), nanoseconds=int(adj_nsec))
                transform = self.tf_buffer.lookup_transform(
                    target_frame,
                    point.header.frame_id,
                    tf_time_adj
                )
                transformed_point = tf2_geometry_msgs.do_transform_point(point, transform)
                return transformed_point
            except Exception:
                # 在彻底回退到最新 TF 之前，短等待一次以给 TF buffer 跟上时间（例如 10ms）
                try:
                    time.sleep(0.01)  # 短阻塞，单位秒
                    # 再次尝试使用消息时间进行 lookup
                    transform = self.tf_buffer.lookup_transform(
                        target_frame,
                        point.header.frame_id,
                        tf_time
                    )
                    transformed_point = tf2_geometry_msgs.do_transform_point(point, transform)
                    return transformed_point
                except Exception:
                    # 再退到使用最新的 TF
                    try:
                        transform = self.tf_buffer.lookup_transform(
                            target_frame,
                            point.header.frame_id,
                            rclpy.time.Time()
                        )
                        transformed_point = tf2_geometry_msgs.do_transform_point(point, transform)
                        return transformed_point
                    except Exception as e2:
                        now_sec = self.get_clock().now().nanoseconds / 1e9
                        if now_sec - self._last_tf_warn_time > 1.0:
                            self.get_logger().warn(f"回退到最新 TF 仍失败: {e2}")
                            self._last_tf_warn_time = now_sec
                        return None

        except LookupException as e:
            # 未找到变换，记录为 debug
            self.get_logger().debug(f"坐标变换未找到: {e}")
            return None

        except Exception as e:
            # 其它错误保留 warn（限频）
            now_sec = self.get_clock().now().nanoseconds / 1e9
            if now_sec - self._last_tf_warn_time > 1.0:
                self.get_logger().warn(f"坐标变换失败: {e}")
                self._last_tf_warn_time = now_sec
            return None
    
    def detect_stationary_state(self, velocity, current_time):
        """检测目标是否处于静止状态"""
        # current_time 可能是 rclpy.time.Time 或已经是浮点秒数
        if hasattr(current_time, 'nanoseconds'):
            current_time_sec = current_time.nanoseconds / 1e9
        else:
            try:
                current_time_sec = float(current_time)
            except Exception:
                current_time_sec = self.get_clock().now().nanoseconds / 1e9
        
        # 如果速度低于阈值
        if velocity < self.velocity_threshold:
            if self.stationary_start_time is None:
                # 开始计时
                self.stationary_start_time = current_time_sec
                self.get_logger().info(f"目标开始静止，速度: {velocity:.3f} m/s")
            else:
                # 检查是否达到静止时间阈值
                stationary_duration = current_time_sec - self.stationary_start_time
                if stationary_duration >= self.stationary_time:
                    self.get_logger().info(f"目标已静止 {stationary_duration:.1f} 秒，触发回收操作")
                    # 暂时注释掉回收触发
                    # self.trigger_collection()
                    self.stationary_start_time = None  # 重置计时器
        else:
            # 目标在移动，重置计时器
            if self.stationary_start_time is not None:
                self.get_logger().info(f"目标恢复运动，速度: {velocity:.3f} m/s")
            self.stationary_start_time = None
        
        self.last_velocity = velocity
    
    # 暂时注释掉回收相关功能
    def trigger_collection(self):
        """触发回收操作"""
        if self.current_target is None:
            self.get_logger().warn("没有目标数据，无法触发回收")
            return
        
        # 检查动作服务器是否可用
        if not self.collect_action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn("回收动作服务器不可用")
            return
        
        # 创建目标
        goal_msg = Collect.Goal()
        goal_msg.x = self.current_target.pose.pose.position.x
        goal_msg.y = self.current_target.pose.pose.position.y
        
        # 发送目标
        self.get_logger().info(f"发送回收目标: ({goal_msg.x:.3f}, {goal_msg.y:.3f})")
        future = self.collect_action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.collection_goal_response_callback)
    
    def collection_goal_response_callback(self, future):
        """回收目标响应回调"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("回收目标被拒绝")
            return
        
        self.get_logger().info("回收目标已接受")
        
        # 获取结果
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.collection_result_callback)
    
    def collection_result_callback(self, future):
        """回收结果回调"""
        try:
            result = future.result().result
            if result.success:
                self.get_logger().info("回收操作成功完成")
            else:
                self.get_logger().warn("回收操作失败")
        except Exception as e:
            self.get_logger().error(f"获取回收结果时出错: {e}")
    
    def publish_timer_callback(self):
        """定时发布目标状态"""
        if self.current_target is not None:
            self.target_publisher.publish(self.current_target)


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = RobotTrackerNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"节点运行出错: {e}")
    finally:
        if 'node' in locals():
            node.destroy_node()
        # 不在每个节点中调用 rclpy.shutdown()，由 launch 管理整体生命周期，
        # 避免在多节点启动/Ctrl-C 时出现重复 shutdown 导致的 RCLError
        return


if __name__ == '__main__':
    main()