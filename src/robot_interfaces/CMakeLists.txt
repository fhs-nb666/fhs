cmake_minimum_required(VERSION 3.8)
project(robot_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖 - 必须在 rosidl_generate_interfaces 之前
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 先查找消息依赖
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# 生成消息和服务
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Target.msg"
  "msg/Control.msg"
  "msg/RobotState.msg"
  "srv/SetMode.srv"
  "action/Collect.action"
  DEPENDENCIES geometry_msgs std_msgs
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()