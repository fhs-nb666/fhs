#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
import math
import threading
import traceback

# 导入自定义消息
from robot_interfaces.msg import Target, Control
from robot_interfaces.srv import SetMode

# TF2相关导入
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs


class RobotSolver(Node):
    def __init__(self):
        super().__init__('robot_solver')
        
        # 声明参数
        self.declare_parameter('bullet_speed', 20.0)
        self.declare_parameter('hit_mode', 'Positive')
        
        # 获取参数
        self.bullet_speed = self.get_parameter('bullet_speed').get_parameter_value().double_value
        self.current_mode = self.get_parameter('hit_mode').get_parameter_value().string_value
        
        # 初始化变量
        self.initial_angle = 0.0
        self.initial_angle_set = False
        self.latest_target = None
        
        # QoS配置 - 使用可靠传输确保数据不丢失
        qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE
        )
        
        # 创建订阅者
        self.target_sub = self.create_subscription(
            Target,
            'robot_tracker/target',
            self.target_callback,
            qos_profile
        )
        
        # 创建发布者
        self.control_pub = self.create_publisher(
            Control,
            'robot_solver/control',
            qos_profile
        )
        
        # 创建服务
        self.mode_service = self.create_service(
            SetMode,
            'robot_solver/set_mode',
            self.set_mode_callback
        )
        
        # TF2相关初始化
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # 锁用于线程安全
        self.lock = threading.Lock()
        
        self.get_logger().info(f'Robot Solver 节点已启动')
        self.get_logger().info(f'当前模式: {self.current_mode}')
        self.get_logger().info(f'子弹速度: {self.bullet_speed} m/s')
    
    def target_callback(self, msg):
        """处理目标状态消息"""
        try:
            with self.lock:
                self.latest_target = msg
            
            # 获取从base_link到world的变换
            transform = self.tf_buffer.lookup_transform(
                'base_link', 
                'world', 
                rclpy.time.Time()
            )
            
            # 将目标位置从world系转换到base_link系
            target_world = PointStamped()
            target_world.header.frame_id = 'world'
            target_world.header.stamp = self.get_clock().now().to_msg()
            target_world.point.x = msg.x
            target_world.point.y = msg.y
            target_world.point.z = 0.0
            
            target_base = self.tf_buffer.transform(target_world, 'base_link')
            
            # 计算目标在base_link系下的角度
            current_angle = math.atan2(target_base.point.y, target_base.point.x) * 180.0 / math.pi
            
            # 如果是第一次收到数据，设置初始角度
            if not self.initial_angle_set:
                self.initial_angle = current_angle
                self.initial_angle_set = True
                self.get_logger().info(f'初始角度设置为: {self.initial_angle:.2f} 度')
            
            # 预测目标未来位置并解算控制指令
            control_msg = self.calculate_control(msg, current_angle)
            
            # 发布控制指令
            self.control_pub.publish(control_msg)
            
        except TransformException as ex:
            # 打印完整 traceback 以便调试 TF 错误
            self.get_logger().warn(f'TF变换错误: {ex}\n{traceback.format_exc()}')
        except Exception as ex:
            # 打印完整 traceback 以便定位崩溃原因
            self.get_logger().error(f'处理目标数据时出错: {ex}\n{traceback.format_exc()}')
    
    def calculate_control(self, target_msg, current_angle):
        """计算控制指令"""
        control_msg = Control()
        
        # 计算目标距离
        distance = math.sqrt(target_msg.x**2 + target_msg.y**2)
        control_msg.distance = distance
        
        # 预测目标未来位置（考虑子弹飞行时间）
        flight_time = distance / self.bullet_speed
        predicted_x = target_msg.x + target_msg.vx * flight_time
        predicted_y = target_msg.y + target_msg.vy * flight_time
        
        # 计算预测位置的角度
        predicted_angle = math.atan2(predicted_y, predicted_x) * 180.0 / math.pi
        
        # 根据模式决定最终角度和开火建议
        if self.current_mode == "Positive":
            # Positive模式：直接跟随预测角度
            control_msg.angle = predicted_angle
            control_msg.fire_cmd = True  # Positive模式持续开火
            
        elif self.current_mode == "Passive":
            # Passive模式：限制在初始角度 ±10° 范围内
            angle_diff = predicted_angle - self.initial_angle
            
            # 归一化角度差到 [-180, 180]
            while angle_diff > 180.0:
                angle_diff -= 360.0
            while angle_diff < -180.0:
                angle_diff += 360.0
            
            if abs(angle_diff) <= 10.0:
                # 在范围内，使用预测角度
                control_msg.angle = predicted_angle
                control_msg.fire_cmd = True
            else:
                # 超出范围，使用边界角度，不开火
                if angle_diff > 0:
                    control_msg.angle = self.initial_angle + 10.0
                else:
                    control_msg.angle = self.initial_angle - 10.0
                control_msg.fire_cmd = False
        
        # 调试信息
        self.get_logger().debug(
            f'模式: {self.current_mode}, 角度: {control_msg.angle:.2f}°, '
            f'距离: {distance:.2f}m, 开火: {"是" if control_msg.fire_cmd else "否"}'
        )
        
        return control_msg
    
    def set_mode_callback(self, request, response):
        """处理模式切换服务请求"""
        new_mode = request.mode
        
        if new_mode in ["Positive", "Passive"]:
            with self.lock:
                self.current_mode = new_mode
            response.success = True
            self.get_logger().info(f'击打模式已切换为: {self.current_mode}')
        else:
            response.success = False
            self.get_logger().warn(f'无效的击打模式: {new_mode}')
        
        return response


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = RobotSolver()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # 输出完整 traceback，帮助定位启动时的异常
        try:
            if 'node' in locals():
                node.get_logger().error(f"节点运行时出错: {e}\n{traceback.format_exc()}")
            else:
                print(f"节点运行时出错: {e}\n{traceback.format_exc()}")
        except Exception:
            print(f"节点运行时出错: {e}")
    finally:
        if 'node' in locals():
            node.destroy_node()
        # 不在每个节点中调用 rclpy.shutdown()，由 launch 管理整体生命周期
        return


if __name__ == '__main__':
    main()