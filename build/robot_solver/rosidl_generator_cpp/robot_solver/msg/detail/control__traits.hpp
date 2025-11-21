// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_solver:msg/Control.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_SOLVER__MSG__DETAIL__CONTROL__TRAITS_HPP_
#define ROBOT_SOLVER__MSG__DETAIL__CONTROL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_solver/msg/detail/control__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_solver
{

namespace msg
{

inline void to_flow_style_yaml(
  const Control & msg,
  std::ostream & out)
{
  out << "{";
  // member: angle
  {
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << ", ";
  }

  // member: fire
  {
    out << "fire: ";
    rosidl_generator_traits::value_to_yaml(msg.fire, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Control & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << "\n";
  }

  // member: fire
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fire: ";
    rosidl_generator_traits::value_to_yaml(msg.fire, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Control & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robot_solver

namespace rosidl_generator_traits
{

[[deprecated("use robot_solver::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_solver::msg::Control & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_solver::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_solver::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_solver::msg::Control & msg)
{
  return robot_solver::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_solver::msg::Control>()
{
  return "robot_solver::msg::Control";
}

template<>
inline const char * name<robot_solver::msg::Control>()
{
  return "robot_solver/msg/Control";
}

template<>
struct has_fixed_size<robot_solver::msg::Control>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robot_solver::msg::Control>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robot_solver::msg::Control>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_SOLVER__MSG__DETAIL__CONTROL__TRAITS_HPP_
