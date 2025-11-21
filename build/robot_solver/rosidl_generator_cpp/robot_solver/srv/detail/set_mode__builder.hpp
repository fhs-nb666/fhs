// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_solver:srv/SetMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_SOLVER__SRV__DETAIL__SET_MODE__BUILDER_HPP_
#define ROBOT_SOLVER__SRV__DETAIL__SET_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_solver/srv/detail/set_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_solver
{

namespace srv
{

namespace builder
{

class Init_SetMode_Request_mode
{
public:
  Init_SetMode_Request_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_solver::srv::SetMode_Request mode(::robot_solver::srv::SetMode_Request::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_solver::srv::SetMode_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_solver::srv::SetMode_Request>()
{
  return robot_solver::srv::builder::Init_SetMode_Request_mode();
}

}  // namespace robot_solver


namespace robot_solver
{

namespace srv
{

namespace builder
{

class Init_SetMode_Response_message
{
public:
  explicit Init_SetMode_Response_message(::robot_solver::srv::SetMode_Response & msg)
  : msg_(msg)
  {}
  ::robot_solver::srv::SetMode_Response message(::robot_solver::srv::SetMode_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_solver::srv::SetMode_Response msg_;
};

class Init_SetMode_Response_success
{
public:
  Init_SetMode_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetMode_Response_message success(::robot_solver::srv::SetMode_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetMode_Response_message(msg_);
  }

private:
  ::robot_solver::srv::SetMode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_solver::srv::SetMode_Response>()
{
  return robot_solver::srv::builder::Init_SetMode_Response_success();
}

}  // namespace robot_solver

#endif  // ROBOT_SOLVER__SRV__DETAIL__SET_MODE__BUILDER_HPP_
