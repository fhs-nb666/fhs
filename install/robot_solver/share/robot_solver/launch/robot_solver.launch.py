from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取参数文件路径
    config_file = os.path.join(
        get_package_share_directory('robot_solver'),
        'config',
        'params.yaml'
    )
    
    return LaunchDescription([
        Node(
            package='robot_solver',
            executable='robot_solver_node',
            name='robot_solver',
            parameters=[config_file],
            output='screen',
            emulate_tty=True
        )
    ])