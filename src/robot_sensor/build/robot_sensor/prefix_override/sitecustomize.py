import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/fhs/ros2_ws/src/robot_sensor/install/robot_sensor'
