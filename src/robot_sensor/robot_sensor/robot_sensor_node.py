import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

import os
import numpy as np

from geometry_msgs.msg import TransformStamped, PointStamped
from tf2_ros import TransformBroadcaster


class RobotSensorNode(Node):
    def __init__(self):
        super().__init__('robot_sensor')
        
        # 声明和获取参数
        params = {
            'data_file_path': 'sensor_data_straight.txt',
            'frequency': 50.0,
            'observation_frame': 'base_link',
            'world_frame': 'world',
            'base_frame': 'base_link',
            'target_frame': 'target_link',
            'topic_name': 'robot_sensor/observed',
            'qos_depth': 10,
            # 是否循环播放，设置为 True 则持续发布（默认改为 True）
            'loop': True
        }
        
        for param, default in params.items():
            self.declare_parameter(param, default)
        
        # 简化参数获取
        self.data_file_path = self.get_parameter('data_file_path').value
        self.frequency = self.get_parameter('frequency').value
        self.observation_frame = self.get_parameter('observation_frame').value
        self.world_frame = self.get_parameter('world_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        self.target_frame = self.get_parameter('target_frame').value
        self.loop = self.get_parameter('loop').value
        # finished 标志用于通知 main 退出 spin 循环（单次模式下）
        self.finished = False
        
        self.get_logger().info(f"启动传感器节点，数据文件: {self.data_file_path}")

        # 读取传感器数据
        self.sensor_data = self._read_sensor_data()
        if not self.sensor_data:
            return
            
        self.current_index = 0
        self.data_length = len(self.sensor_data)
        
        # 创建发布者和TF广播器
        qos_profile = QoSProfile(
            depth=self.get_parameter('qos_depth').value,
            reliability=ReliabilityPolicy.RELIABLE
        )
        
        # 使用 geometry_msgs/PointStamped
        self.publisher = self.create_publisher(
            PointStamped,
            self.get_parameter('topic_name').value, 
            qos_profile
        )
        
        # 确保TF广播器正确初始化
        self.tf_broadcaster = TransformBroadcaster(self)
        self.get_logger().info("TF广播器初始化完成")
        
        # 创建定时器 (frequency Hz)
        self.timer = self.create_timer(1.0/self.frequency, self._timer_callback)
        
        self.get_logger().info(f"成功读取 {self.data_length} 条数据，开始循环发布...")
        self.get_logger().info("使用 PointStamped 消息类型")
    
    def _read_sensor_data(self):
        """读取传感器数据文件"""
        file_path = self._resolve_file_path(self.data_file_path)
        
        if not os.path.exists(file_path):
            self.get_logger().error(f"数据文件不存在: {file_path}")
            return []
            
        try:
            data = []
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            data.append((float(parts[0]), float(parts[1])))
                        except ValueError:
                            self.get_logger().warning(f"第 {line_num} 行数据格式错误")
            
            self.get_logger().info(f"从文件读取 {len(data)} 条有效数据")
            return data
            
        except Exception as e:
            self.get_logger().error(f"读取数据文件失败: {e}")
            return []
    
    def _resolve_file_path(self, file_path):
        """解析文件路径"""
        if os.path.isabs(file_path):
            return file_path
            
        package_share_dir = self.get_package_share_directory('robot_sensor')
        possible_paths = [
            file_path,
            os.path.join(package_share_dir, file_path),
            os.path.join(package_share_dir, 'data', os.path.basename(file_path))
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        return file_path
    
    def _timer_callback(self):
        """定时器回调函数 - 100Hz频率,循环播放"""
        # 如果到达数据末尾，根据参数决定是否循环播放
        if self.current_index >= self.data_length:
            if self.loop:
                self.current_index = 0
                self.get_logger().info("数据播放完成，重新开始循环播放")
            else:
                # 停止定时器，结束单次播放
                self.get_logger().info("数据播放完成，停止发布（单次模式）")
                try:
                    # cancel() 在 rclpy 的 Timer 对象上可用
                    if self.timer is not None:
                        self.timer.cancel()
                except Exception:
                    pass
                # 标记为完成，main 中的 spin_once 循环会退出，随后进程清理并结束
                self.finished = True
                return
        
        # 发布传感器数据 -- 使用同一时间戳用于消息与 TF 广播，避免时间对齐问题
        x, y = self.sensor_data[self.current_index]

        # 获取当前时刻并将时间戳提前以减少 tracker 端查询未来时间的概率
        now_time = self.get_clock().now()
        adj_ns_total = now_time.nanoseconds - 10_000_000  # 提前 10ms
        if adj_ns_total < 0:
            adj_ns_total = 0
        adj_sec = int(adj_ns_total // 1_000_000_000)
        adj_nsec = int(adj_ns_total % 1_000_000_000)
        adj_time = rclpy.time.Time(seconds=adj_sec, nanoseconds=adj_nsec)
        now_msg = adj_time.to_msg()

        msg = PointStamped()
        msg.header.stamp = now_msg
        msg.header.frame_id = self.observation_frame
        msg.point.x = x
        msg.point.y = y
        msg.point.z = 0.0

        self.publisher.publish(msg)

        # 广播TF变换，使用相同时间戳
        self._broadcast_tf(x, y, now_msg)
        
        self.current_index += 1
        
        # 进度显示（减少日志输出频率）
        if self.current_index % 200 == 0:
            progress = (self.current_index / self.data_length) * 100
            self.get_logger().info(f"发布进度: {progress:.1f}% ({self.current_index}/{self.data_length})")
    
    def _broadcast_tf(self, x, y, current_time_msg=None):
        """广播TF坐标系变换 - 包含 world, base_link, target_link"""
        # 如果传入了时间戳参数则使用该时间，否则回退到节点当前时间
        current_time = current_time_msg if current_time_msg is not None else self.get_clock().now().to_msg()
        # world -> base_link 变换
        transform1 = TransformStamped()
        transform1.header.stamp = current_time
        transform1.header.frame_id = self.world_frame
        transform1.child_frame_id = self.base_frame
        transform1.transform.translation.x = 0.0
        transform1.transform.translation.y = 0.0
        transform1.transform.translation.z = 0.0
        transform1.transform.rotation.x = 0.0
        transform1.transform.rotation.y = 0.0
        transform1.transform.rotation.z = 0.0
        transform1.transform.rotation.w = 1.0
        
        # base_link -> target_link 变换
        transform2 = TransformStamped()
        transform2.header.stamp = current_time
        transform2.header.frame_id = self.base_frame
        transform2.child_frame_id = self.target_frame
        transform2.transform.translation.x = x
        transform2.transform.translation.y = y
        transform2.transform.translation.z = 0.0
        transform2.transform.rotation.x = 0.0
        transform2.transform.rotation.y = 0.0
        transform2.transform.rotation.z = 0.0
        transform2.transform.rotation.w = 1.0
        
        # 发送TF变换
        self.tf_broadcaster.sendTransform([transform1, transform2])


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = RobotSensorNode()
        # 如果是循环模式（持续发布），直接 spin；否则使用 spin_once 以便在单次发布完成后退出
        if getattr(node, 'loop', False):
            rclpy.spin(node)
        else:
            while rclpy.ok() and not getattr(node, 'finished', False):
                rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"节点运行出错: {e}")
    finally:
        if 'node' in locals():
            node.destroy_node()
        # 由 launch 管理 shutdown，避免重复调用导致的 RCLError
        return


if __name__ == '__main__':
    main()