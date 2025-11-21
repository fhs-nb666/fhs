// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:msg/Target.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__TARGET__STRUCT_H_
#define ROBOT_INTERFACES__MSG__DETAIL__TARGET__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/Target in the package robot_interfaces.
typedef struct robot_interfaces__msg__Target
{
  std_msgs__msg__Header header;
  float x;
  float y;
  float vx;
  float vy;
} robot_interfaces__msg__Target;

// Struct for a sequence of robot_interfaces__msg__Target.
typedef struct robot_interfaces__msg__Target__Sequence
{
  robot_interfaces__msg__Target * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__msg__Target__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__TARGET__STRUCT_H_
