from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    ld = LaunchDescription()

    # 包的 launch 文件路径
    pkg_names = [
        'robot_sensor',
        'robot_tracker',
        'robot_solver',
        'robot_controller',
    ]

    for pkg in pkg_names:
        try:
            share_dir = get_package_share_directory(pkg)
            launch_file = os.path.join(share_dir, 'launch', f'{pkg}.launch.py')
            if os.path.exists(launch_file):
                ld.add_action(
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(launch_file)
                    )
                )
        except Exception:
            # 如果某个包不存在或没有 launch，忽略并继续
            pass

    return ld
