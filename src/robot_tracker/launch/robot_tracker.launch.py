from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    robot_tracker_node = Node(
        package='robot_tracker',
        executable='robot_tracker_node',
        name='robot_tracker',
        output='screen',
        parameters=[os.path.join(get_package_share_directory('robot_tracker'), 
           'config', 'params.yaml')]         
    )
    return LaunchDescription([
        robot_tracker_node
    ])