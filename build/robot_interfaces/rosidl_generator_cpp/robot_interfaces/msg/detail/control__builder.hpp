// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Control.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__CONTROL__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Control_fire
{
public:
  explicit Init_Control_fire(::robot_interfaces::msg::Control & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Control fire(::robot_interfaces::msg::Control::_fire_type arg)
  {
    msg_.fire = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Control msg_;
};

class Init_Control_angle
{
public:
  explicit Init_Control_angle(::robot_interfaces::msg::Control & msg)
  : msg_(msg)
  {}
  Init_Control_fire angle(::robot_interfaces::msg::Control::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return Init_Control_fire(msg_);
  }

private:
  ::robot_interfaces::msg::Control msg_;
};

class Init_Control_header
{
public:
  Init_Control_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Control_angle header(::robot_interfaces::msg::Control::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Control_angle(msg_);
  }

private:
  ::robot_interfaces::msg::Control msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Control>()
{
  return robot_interfaces::msg::builder::Init_Control_header();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__CONTROL__BUILDER_HPP_
