from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'robot_sensor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'data'), glob('data/*.txt')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fhs',
    maintainer_email='fhs@todo.todo',
    description='Robot sensor simulation node',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_sensor_node = robot_sensor.robot_sensor_node:main',
            'generate_sensor_data = robot_sensor.generate_sensor_data:main',
        ],
    },
)