// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_RobotState_y
{
public:
  explicit Init_RobotState_y(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::RobotState y(::robot_interfaces::msg::RobotState::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_x
{
public:
  explicit Init_RobotState_x(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_y x(::robot_interfaces::msg::RobotState::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_RobotState_y(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_header
{
public:
  Init_RobotState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotState_x header(::robot_interfaces::msg::RobotState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RobotState_x(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::RobotState>()
{
  return robot_interfaces::msg::builder::Init_RobotState_header();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
