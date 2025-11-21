// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_solver:msg/Control.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_SOLVER__MSG__DETAIL__CONTROL__BUILDER_HPP_
#define ROBOT_SOLVER__MSG__DETAIL__CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_solver/msg/detail/control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_solver
{

namespace msg
{

namespace builder
{

class Init_Control_fire
{
public:
  explicit Init_Control_fire(::robot_solver::msg::Control & msg)
  : msg_(msg)
  {}
  ::robot_solver::msg::Control fire(::robot_solver::msg::Control::_fire_type arg)
  {
    msg_.fire = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_solver::msg::Control msg_;
};

class Init_Control_angle
{
public:
  Init_Control_angle()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Control_fire angle(::robot_solver::msg::Control::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return Init_Control_fire(msg_);
  }

private:
  ::robot_solver::msg::Control msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_solver::msg::Control>()
{
  return robot_solver::msg::builder::Init_Control_angle();
}

}  // namespace robot_solver

#endif  // ROBOT_SOLVER__MSG__DETAIL__CONTROL__BUILDER_HPP_
