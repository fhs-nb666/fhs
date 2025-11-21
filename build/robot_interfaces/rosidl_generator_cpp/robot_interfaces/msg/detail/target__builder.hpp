// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/Target.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__TARGET__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__TARGET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/target__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_Target_vy
{
public:
  explicit Init_Target_vy(::robot_interfaces::msg::Target & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::Target vy(::robot_interfaces::msg::Target::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::Target msg_;
};

class Init_Target_vx
{
public:
  explicit Init_Target_vx(::robot_interfaces::msg::Target & msg)
  : msg_(msg)
  {}
  Init_Target_vy vx(::robot_interfaces::msg::Target::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_Target_vy(msg_);
  }

private:
  ::robot_interfaces::msg::Target msg_;
};

class Init_Target_y
{
public:
  explicit Init_Target_y(::robot_interfaces::msg::Target & msg)
  : msg_(msg)
  {}
  Init_Target_vx y(::robot_interfaces::msg::Target::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Target_vx(msg_);
  }

private:
  ::robot_interfaces::msg::Target msg_;
};

class Init_Target_x
{
public:
  explicit Init_Target_x(::robot_interfaces::msg::Target & msg)
  : msg_(msg)
  {}
  Init_Target_y x(::robot_interfaces::msg::Target::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Target_y(msg_);
  }

private:
  ::robot_interfaces::msg::Target msg_;
};

class Init_Target_header
{
public:
  Init_Target_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Target_x header(::robot_interfaces::msg::Target::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Target_x(msg_);
  }

private:
  ::robot_interfaces::msg::Target msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::Target>()
{
  return robot_interfaces::msg::builder::Init_Target_header();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__TARGET__BUILDER_HPP_
