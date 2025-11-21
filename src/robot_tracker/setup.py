from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'robot_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 安装配置文件
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        # 安装launch文件
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fhs',
    maintainer_email='fhs@todo.todo',
    description='Robot tracker for target state estimation and collection',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_tracker_node = robot_tracker.robot_tracker_node:main',
        ],
    },
)