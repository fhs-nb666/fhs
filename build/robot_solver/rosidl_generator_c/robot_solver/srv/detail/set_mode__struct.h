// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_solver:srv/SetMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_SOLVER__SRV__DETAIL__SET_MODE__STRUCT_H_
#define ROBOT_SOLVER__SRV__DETAIL__SET_MODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'mode'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetMode in the package robot_solver.
typedef struct robot_solver__srv__SetMode_Request
{
  rosidl_runtime_c__String mode;
} robot_solver__srv__SetMode_Request;

// Struct for a sequence of robot_solver__srv__SetMode_Request.
typedef struct robot_solver__srv__SetMode_Request__Sequence
{
  robot_solver__srv__SetMode_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_solver__srv__SetMode_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetMode in the package robot_solver.
typedef struct robot_solver__srv__SetMode_Response
{
  /// 是否成功
  bool success;
  /// 相应的消息
  rosidl_runtime_c__String message;
} robot_solver__srv__SetMode_Response;

// Struct for a sequence of robot_solver__srv__SetMode_Response.
typedef struct robot_solver__srv__SetMode_Response__Sequence
{
  robot_solver__srv__SetMode_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_solver__srv__SetMode_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_SOLVER__SRV__DETAIL__SET_MODE__STRUCT_H_
