#!/usr/bin/python3.10
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

import math
import numpy as np
from typing import Optional, Tuple

from geometry_msgs.msg import PointStamped
from robot_solver.msg import Control
from robot_solver.srv import SetMode

class RobotSolverNode(Node):
    def __init__(self):
        super().__init__('robot_solver')

        # Load parameters
        self.declare_parameter()

        # 状态变量
        self.current_mode = "Position"
        self.initial_angle = None
        self.last_target_time = None
        self.target_velocity = np.array([0.0, 0.0])
        self.velocity_alpha = self.get_parameter('velocity_smoothing').value 

        # 创建订阅者
        self.target_subscriber = self.create_subscription(
            PointStamped,
            'target_position',
            self.target_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )

        # 创建发布者
        self.control_publisher = self.create_publisher(
            Control,
            'robot_solver/control',
            10
        )

        # 创建服务
        self.mode_service = self.create_service(
            SetMode,
            'robot_solver/set_mode',
            self.set_mode_callback
        )

        self.get_logger().info("机器人解算节点已启动")
        self.get_logger().info(f"当前模式: {self.current_mode}")
        self.get_logger().info(f"子弹速度: {self.get_parameter('bullet_speed').value} m/s")
        self.get_logger().info(f"目标半径: {self.get_parameter('target_radius').value} m")
        self.get_logger().info(f"Passive模式角度限制: ±{self.get_parameter('max_passive_angle').value}°")

        def declare_parameter(self):
            # "声明所有参数"
            parameters = {
                'bullet_speed': 20.0,
                'target_radius': 0.25,
                'max_passive_angle': 10, 
                'prediction_enabled': True,
                'velocity_smoothing': 0.8
            }
            for param, default in parameters.items():
                self.declare_parameter(param, default) 

        def set_mode_callback(self, request, response):
            # "处理设置模式服务请求"
            mode = request.mode.strip()

            if mode.lower() =="position":
                self.current_mode = "Position"
                self.initial_angle = None  # 重置初始角度
                response.success = True
                response.message = "模式已切换到 Position"
                self.get_logger().info(response.message)

            elif mode.lower() =="passive":
                self.current_mode = "Passive"
                response.success = True
                response.message = "模式已切换到 Passive"
                self.get_logger().info(response.message)
                self.get_logger().info("等待第一个目标位置来设置初始角度...")

            else:
                response.success = False
                response.message = f"未知模式: {mode}. 可用模式: Position, Passive"
                self.get_logger().warn(response.message)

            return response
        
    def target_callback(self, msg: PointStamped):
        # "处理目标位置更新"
        try:
            # "提取当前位置"
            current_position = np.array([msg.point.x, msg.point.y])
            current_time = self.get_clock().now()

            # "更新目标速度"
            self.update_target_velocity(current_position, current_time)

            # "预计目标位置"
            if self.get_parameter('prediction_enabled').value:
                target_position = self.predict_target_position(current_position)
            else:
                target_position = current_position

            # "计算击打角度"
            fire_angle = self.cauculate_fire_angle(target_position)

            # "决定是否开火"
            should_fire = self.should_fire(target_position, fire_angle)

            # "发布控制命令"
            self.publish_control(fire_angle, should_fire, msg.header.stamp)



        except Exception as e:
            self.get_logger().error(f"处理目标位置时出错: {e}")

    def update_velocity_estimate(self, current_position: np.ndarray, current_time: rclpy.time.Time ):
        # "更新目标速度估计"
        if self.last_target_time is not None and self.last_target_time is not None:
            # "计算时间差"
            dt = (current_time - self.last_target_time).nanoseconds / 1e-9

            if dt > 0:
                # 计算瞬时速度
                instant_velocity = (current_position - self.last_target_position) / dt

                # 计算平滑滤波
                self.target_velocity = (self.velocity_alpha * instant_velocity +
                                        (1 - self.velocity_alpha) * self.target_velocity)
        # 更新最后位置和时间
        self.last_target_position = current_position
        self.last_target_time = current_time
    
    def predict_target_position(self, current_position: np.ndarray) -> np.ndarray:
        # "预测未来位置"
        bullet_speed = self.get_parameter('bullet_speed').value
        
        # "计算距离和时间"
        distance = np.linalg.norm(current_position)

        if distance == 0:
            return current_position
        
        # "计算子弹飞行时间"
        fligent_time = distance / bullet_speed

        # 如果速度很小不进行预测
        speed_norm = np.linalg.norm(self.target_velocity)
        if speed_norm < 0.01:
            return current_position
        
        # 预测位置
        predicted_position = current_position + self.target_velocity * fligent_time
        
        #调试信息
        if self.get_logger().get_effective_level() <= 10:  # DEBUG level
            self.get_logger().debug(
                f"预测: 当前位置 ({current_position[0]:.2f}, {current_position[1]:.2f}) -> "
                f"预测位置 ({predicted_position[0]:.2f}, {predicted_position[1]:.2f})"
            )
         
        return predicted_position
    
    def cauculate_fire_angle(self, target_position: np.ndarray) -> float:
        # "计算击打角度"
        x,y = target_position

        # 计算原始角度
        angle_red = math.atan2(y, x)
        angle_deg = math.degrees(angle_red)

        # Passive模式下应用角度限制
        if self.current_mode == "Passive":
                        # 设置初始角度（如果还没有设置）
            if self.initial_angle is None:
                self.initial_angle = angle_deg
                self.get_logger().info(f"Passive模式初始角度设置为: {self.initial_angle:.1f}°")

            # 计算角度偏差
            angle_diff = angle_deg - self.initial_angle

            # 角度归一化
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360

            # 应用角度限制
            max_angle = self.get_parameter('max_passive_angle').value
            if abs(angle_diff) > max_angle:
                if angle_diff > 0:
                    angle_deg = self.initial_angle + max_angle
                else:
                    angle_deg = self.initial_angle - max_angle

            self.get_logger().debug( f"角度受限: 原始{angle_deg:.1f}° -> 限制后{angle_deg:.1f}° "
                    f"(限制范围: ±{max_angle}°)"
                )
        return angle_deg
    
    def should_fire(self, target_position: np.ndarray, fire_angle: float) -> bool:
        # "决定是否开火"
        target_radius = self.get_parameter('target_radius').value

        # 计算到目标的距离
        distance = np.linalg.norm(target_position)

        # 基础条件：目标必须在子弹射程内
        if distance > target_radius:
            return False
        
        # Passive 模式额外检查角度限制
        if self.current_mode == "Passive" and self.initial_angle is not None:
            angle_diff = abs(fire_angle - self.initial_angle)

            # 角度归一化
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360

            max_angle = self.get_parameter('max_passive_angle').value
            if abs(angle_diff) > max_angle:
                return False
            
        return True
    
    def publish_control(self, angle: float, fire: bool, timestamp):
        #发布控制指令
        control_msg = Control()
        control_msg.angle = angle
        control_msg.fire = fire
        control_msg.header.stamp = timestamp

        self.control_publisher.publish(control_msg)

        # 记录开火决策
        if fire:
            mode_info = ""
            if self.current_mode == "Passive":
                mode_info = f" (初始角度: {self.initial_angle:.1f}°)"

            self.get_logger().info(
                f"开火! 角度: {angle:.1f}°{mode_info}"
            )  
        else:
            self.get_logger().debug(f"不开火。 角度: {angle:.1f}°")


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = RobotSolverNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"节点运行出错: {e}")
    finally:
        if 'node' in locals():
            node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()










