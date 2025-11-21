// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_solver:msg/Control.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_SOLVER__MSG__DETAIL__CONTROL__STRUCT_H_
#define ROBOT_SOLVER__MSG__DETAIL__CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Control in the package robot_solver.
typedef struct robot_solver__msg__Control
{
  /// 开火角度
  float angle;
  /// 是否开火
  bool fire;
} robot_solver__msg__Control;

// Struct for a sequence of robot_solver__msg__Control.
typedef struct robot_solver__msg__Control__Sequence
{
  robot_solver__msg__Control * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_solver__msg__Control__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_SOLVER__MSG__DETAIL__CONTROL__STRUCT_H_
