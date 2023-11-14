from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dev_robot',
            executable='cmdvel_sub',
            name='robot_drive_node',
            output='screen'
        ),
        Node(
            package='dev_robot',
            executable='encoder_pub',
            name='encoder_publisher_node',
            output='screen'
        ),
        Node(
            package='dev_robot',
            executable='odometery',
            name='odometery_node',
            output='screen'
        ),
    ])