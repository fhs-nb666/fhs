// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:action/Collect.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__ACTION__DETAIL__COLLECT__BUILDER_HPP_
#define ROBOT_INTERFACES__ACTION__DETAIL__COLLECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/action/detail/collect__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_Goal_y
{
public:
  explicit Init_Collect_Goal_y(::robot_interfaces::action::Collect_Goal & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::action::Collect_Goal y(::robot_interfaces::action::Collect_Goal::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_Goal msg_;
};

class Init_Collect_Goal_x
{
public:
  Init_Collect_Goal_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Collect_Goal_y x(::robot_interfaces::action::Collect_Goal::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Collect_Goal_y(msg_);
  }

private:
  ::robot_interfaces::action::Collect_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_Goal>()
{
  return robot_interfaces::action::builder::Init_Collect_Goal_x();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_Result_success
{
public:
  Init_Collect_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::action::Collect_Result success(::robot_interfaces::action::Collect_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_Result>()
{
  return robot_interfaces::action::builder::Init_Collect_Result_success();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_Feedback_distance
{
public:
  Init_Collect_Feedback_distance()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::action::Collect_Feedback distance(::robot_interfaces::action::Collect_Feedback::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_Feedback>()
{
  return robot_interfaces::action::builder::Init_Collect_Feedback_distance();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_SendGoal_Request_goal
{
public:
  explicit Init_Collect_SendGoal_Request_goal(::robot_interfaces::action::Collect_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::action::Collect_SendGoal_Request goal(::robot_interfaces::action::Collect_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_SendGoal_Request msg_;
};

class Init_Collect_SendGoal_Request_goal_id
{
public:
  Init_Collect_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Collect_SendGoal_Request_goal goal_id(::robot_interfaces::action::Collect_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Collect_SendGoal_Request_goal(msg_);
  }

private:
  ::robot_interfaces::action::Collect_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_SendGoal_Request>()
{
  return robot_interfaces::action::builder::Init_Collect_SendGoal_Request_goal_id();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_SendGoal_Response_stamp
{
public:
  explicit Init_Collect_SendGoal_Response_stamp(::robot_interfaces::action::Collect_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::action::Collect_SendGoal_Response stamp(::robot_interfaces::action::Collect_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_SendGoal_Response msg_;
};

class Init_Collect_SendGoal_Response_accepted
{
public:
  Init_Collect_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Collect_SendGoal_Response_stamp accepted(::robot_interfaces::action::Collect_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Collect_SendGoal_Response_stamp(msg_);
  }

private:
  ::robot_interfaces::action::Collect_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_SendGoal_Response>()
{
  return robot_interfaces::action::builder::Init_Collect_SendGoal_Response_accepted();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_GetResult_Request_goal_id
{
public:
  Init_Collect_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::action::Collect_GetResult_Request goal_id(::robot_interfaces::action::Collect_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_GetResult_Request>()
{
  return robot_interfaces::action::builder::Init_Collect_GetResult_Request_goal_id();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_GetResult_Response_result
{
public:
  explicit Init_Collect_GetResult_Response_result(::robot_interfaces::action::Collect_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::action::Collect_GetResult_Response result(::robot_interfaces::action::Collect_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_GetResult_Response msg_;
};

class Init_Collect_GetResult_Response_status
{
public:
  Init_Collect_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Collect_GetResult_Response_result status(::robot_interfaces::action::Collect_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Collect_GetResult_Response_result(msg_);
  }

private:
  ::robot_interfaces::action::Collect_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_GetResult_Response>()
{
  return robot_interfaces::action::builder::Init_Collect_GetResult_Response_status();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace action
{

namespace builder
{

class Init_Collect_FeedbackMessage_feedback
{
public:
  explicit Init_Collect_FeedbackMessage_feedback(::robot_interfaces::action::Collect_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::action::Collect_FeedbackMessage feedback(::robot_interfaces::action::Collect_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::action::Collect_FeedbackMessage msg_;
};

class Init_Collect_FeedbackMessage_goal_id
{
public:
  Init_Collect_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Collect_FeedbackMessage_feedback goal_id(::robot_interfaces::action::Collect_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Collect_FeedbackMessage_feedback(msg_);
  }

private:
  ::robot_interfaces::action::Collect_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::action::Collect_FeedbackMessage>()
{
  return robot_interfaces::action::builder::Init_Collect_FeedbackMessage_goal_id();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__ACTION__DETAIL__COLLECT__BUILDER_HPP_
