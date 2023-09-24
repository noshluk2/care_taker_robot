#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

// The TurtlesimStraightLine node
class TurtlesimStraightLine : public rclcpp::Node {
  public:
    TurtlesimStraightLine() : Node("turtlesim_straight_line") {
      // Set up a publisher and a timer
      cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
      cmd_vel_pub2_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle2/cmd_vel", 10); 
      timer_ = this->create_wall_timer(std::chrono::milliseconds(100),
                                       std::bind(&TurtlesimStraightLine::timer_callback, this));
    }

  private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub2_;
    rclcpp::TimerBase::SharedPtr timer_;

    void timer_callback() {
      // The callback function creates a Twist message with a linear velocity,
      // which will make the turtle move in a straight line, and publishes the message.
      geometry_msgs::msg::Twist twist;
      twist.linear.x = -2;
      twist.angular.z = 1.57;
      cmd_vel_pub_->publish(twist);      
      cmd_vel_pub2_->publish(twist);
    }
};

int main(int argc, char **argv) {
  // Initialize ROS, create the TurtlesimStraightLine node, and spin it
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TurtlesimStraightLine>());
  rclcpp::shutdown();
  return 0;
}