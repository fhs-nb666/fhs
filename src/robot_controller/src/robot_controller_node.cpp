#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include <memory>
#include "robot_interfaces/action/collect.hpp"
#include "geometry_msgs/msg/point.hpp"
#include <cmath>
#include <memory>
#include <rclcpp_action/server.hpp>
#include <rclcpp_action/types.hpp>
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2_ros/transform_broadcaster.h"


using namespace std::chrono_literals; //时间单位
using Collect = robot_interfaces::action::Collect; //定义别名

//类定义与节点初始化
class RobotControllerNode : public rclcpp::Node
{
public:
    using CollectGoalHandle = rclcpp_action::ServerGoalHandle<Collect>;
    //构造函数：初始化节点和动作服务器
    RobotControllerNode() : Node("robot_controller_node"){
        //声明并获取参数
        this->declare_parameter<double>("micro_robot_speed", 3.0);
        micro_robot_speed_ = this->get_parameter("micro_robot_speed").as_double();
        //智能指针初始化变换广播器
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        //创建动作服务器
        action_server_ = rclcpp_action::create_server<Collect>(
            this,
            "collect",
            std::bind(&RobotControllerNode::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
            std::bind(&RobotControllerNode::handle_cancel, this, std::placeholders::_1),
            std::bind(&RobotControllerNode::handle_accepted, this, std::placeholders::_1)
        );
        RCLCPP_INFO(this->get_logger(), "robot_controller_node started! speed=%.2f m/s", micro_robot_speed_);
    }
//完整的动作服务器生命周期
// 客户端发送目标请求
//     ↓
// handle_goal(uuid, goal) 被调用
//     ↓ 返回 ACCEPT_AND_EXECUTE
// handle_accepted(goal_handle) 被调用  
//     ↓ 在新线程中
// execute(goal_handle) 开始执行回收任务
//     ↓ 期间如果客户端取消
// handle_cancel(goal_handle) 被调用
//     ↓ 返回 ACCEPT
// execute() 检测到取消，提前结束
private:
    double micro_robot_speed_; //微型机器人速度参数
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_; //变换广播器智能指针
    rclcpp_action::Server<Collect>::SharedPtr action_server_; //动作服务器智能指针

    //处理目标请求
    rclcpp_action::GoalResponse handle_goal(const rclcpp_action::GoalUUID & ,
        std::shared_ptr<const Collect::Goal>)
        {
            return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
        }

    rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<CollectGoalHandle> )
        {
            RCLCPP_INFO(this->get_logger(), "Received request to cancel goal");
            return rclcpp_action::CancelResponse::ACCEPT;
        }
    
    void handle_accepted(const std::shared_ptr<CollectGoalHandle> goal_handle)
        {
            std::thread{std::bind(&RobotControllerNode::execute, this, goal_handle)}.detach();
        }

    //制微型机器人从当前位置移动到目标位置，并实时反馈进度。
    void execute(const std::shared_ptr<CollectGoalHandle> goal_handle)
        {
            //获取目标位置
            const auto goal = goal_handle->get_goal();
            double target_x = goal->x;
            double target_y = goal->y;
            double curr_x = 0.0;
            double curr_y = 0.0;
            //控制发布频率
            rclcpp::Rate loop_rate(50);
            bool success = false;

            while (rclcpp::ok()){
                //计算距离
                double dx = target_x - curr_x;
                double dy = target_y - curr_y;
                double distance = std::hypot(dx  , dy );

                //发送反馈
                auto feedback = std::make_shared<Collect::Feedback>();
                feedback->distance = distance;
                goal_handle->publish_feedback(feedback);

                //广播TF 和 micro_base_link
                geometry_msgs::msg::TransformStamped t;
                t.header.stamp = this->now();
                t.header.frame_id = "world";
                t.child_frame_id = "micro_base_link";
                t.transform.translation.x = curr_x;
                t.transform.translation.y = curr_y;
                t.transform.translation.z = 0.0;
                t.transform.rotation.x = 0.0;
                t.transform.rotation.y = 0.0;
                t.transform.rotation.z = 0.0;
                t.transform.rotation.w = 1.0;
                tf_broadcaster_->sendTransform(t);

                //判断是否回收完成
                if (distance < 0.5){
                    success = true;
                    RCLCPP_INFO(this->get_logger(), "Reach target, collect success!");
                    break;
                }

                //计算下一步运动
                double step = micro_robot_speed_ / 50.0; 
                if (distance > step){
                    double angle = std::atan2(dy, dx);
                    curr_x += step * std::cos(angle);
                    curr_y += step * std::sin(angle);

                } else {
                    curr_x = target_x;
                    curr_y = target_y;
                }
                //处理被取消
                if (goal_handle->is_canceling()){
                    auto result  = std::make_shared<Collect::Result>();
                    result->success = false;
                    goal_handle->canceled(result);
                    RCLCPP_INFO(this->get_logger(), "Goal canceled");
                    return;
                }

                loop_rate.sleep();

                //结束循环
                if (rclcpp::ok() == false){
                    auto result  = std::make_shared<Collect::Result>();
                    result->success = success;
                    goal_handle->succeed(result);
                }
            }
    }
  
};


int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RobotControllerNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}