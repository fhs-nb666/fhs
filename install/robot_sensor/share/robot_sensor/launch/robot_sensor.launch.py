from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取包共享目录路径
    package_share_dir = get_package_share_directory('robot_sensor')
    # 参数文件路径
    params_file = os.path.join(package_share_dir, 'config', 'params.yaml')
    # 数据文件路径
    data_file_path = os.path.join(package_share_dir, 'data', 'sensor_data_straight.txt')
    
    return LaunchDescription([
        Node(
            package='robot_sensor',
            executable='robot_sensor_node',
            name='robot_sensor',
            output='screen',
            parameters=[
                params_file,
                # 可以覆盖参数文件中的特定参数
                {'data_file_path': data_file_path}
            ]
        ),
    ])