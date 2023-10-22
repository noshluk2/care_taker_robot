import rclpy
from rclpy.node import Node
from math import sin, cos, pi
from geometry_msgs.msg import Quaternion, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from std_msgs.msg import Int16
from geometry_msgs.msg import TransformStamped



class DiffTf(Node):

    def __init__(self):
        super().__init__('diff_tf')

        #### parameters #######
        self.rate = self.declare_parameter("rate", 10.0).value
        self.ticks_meter = float(self.declare_parameter("ticks_meter", 99522.293).value)
        self.base_width = float(self.declare_parameter("base_width", 0.210).value)
        self.base_frame_id = self.declare_parameter("base_frame_id", "base_link").value
        self.odom_frame_id = self.declare_parameter("odom_frame_id", "odom").value
        self.encoder_min = self.declare_parameter("encoder_min", -32768).value
        self.encoder_max = self.declare_parameter("encoder_max", 32768).value
        self.encoder_low_wrap = self.declare_parameter("wheel_low_wrap", (self.encoder_max - self.encoder_min) * 0.3 + self.encoder_min).value
        self.encoder_high_wrap = self.declare_parameter("wheel_high_wrap", (self.encoder_max - self.encoder_min) * 0.7 + self.encoder_min).value

        # internal data
        self.enc_left = None
        self.enc_right = None
        self.left = 0
        self.right = 0
        self.lmult = 0
        self.rmult = 0
        self.prev_lencoder = 0
        self.prev_rencoder = 0
        self.x = 0.0
        self.y = 0.0
        self.th = 0
        self.dx = 0
        self.dr = 0
        self.then = self.get_clock().now()

        # subscriptions and publishers
        self.create_subscription(Int16, '/left_enc', self.lwheelCallback, 10)
        self.create_subscription(Int16, '/right_enc', self.rwheelCallback, 10)
        self.odomPub = self.create_publisher(Odometry, 'odom', 10)
        self.odomBroadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(1.0 / self.rate, self.update)

    def update(self):
        now = self.get_clock().now()
        elapsed = now - self.then
        self.then = now
        elapsed = elapsed.nanoseconds * 1e-9
         # calculate odometry
        if self.enc_left == None:
            d_left = 0
            d_right = 0
        else:
            d_left = (self.left - self.enc_left) / self.ticks_meter
            d_right = (self.right - self.enc_right) / self.ticks_meter
        self.enc_left = self.left
        self.enc_right = self.right

        # distance traveled is the average of the two wheels
        d = ( d_left + d_right ) / 2
        # this approximation works (in radians) for small angles
        th = ( d_right - d_left ) / self.base_width
        # calculate velocities
        self.dx = d / elapsed
        self.dr = th / elapsed


        if (d != 0):
            # calculate distance traveled in x and y
            x = cos( th ) * d
            y = -sin( th ) * d
            # calculate the final position of the robot
            self.x = self.x + ( cos( self.th ) * x - sin( self.th ) * y )
            self.y = self.y + ( sin( self.th ) * x + cos( self.th ) * y )
        if( th != 0):
            self.th = self.th + th

        # publish the odom information
        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = sin( self.th / 2 )
        quaternion.w = cos( self.th / 2 )

        # Create a TransformStamped message
        t = TransformStamped()

        # Fill in the details for the transform
        t.header.stamp = self.get_clock().now().to_msg()  # ROS 2 time representation
        t.header.frame_id = self.odom_frame_id
        t.child_frame_id = self.base_frame_id
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = quaternion.x
        t.transform.rotation.y = quaternion.y
        t.transform.rotation.z = quaternion.z
        t.transform.rotation.w = quaternion.w

        # Broadcast the transform
        self.odomBroadcaster.sendTransform(t)

        # Odometry message
        odom = Odometry()
        # Correct
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = self.odom_frame_id
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = quaternion
        odom.child_frame_id = self.base_frame_id
        odom.twist.twist.linear.x = self.dx
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = self.dr
        self.odomPub.publish(odom)



    def lwheelCallback(self, msg):
        enc = msg.data
        if (enc < self.encoder_low_wrap and self.prev_lencoder > self.encoder_high_wrap):
            self.lmult = self.lmult + 1

        if (enc > self.encoder_high_wrap and self.prev_lencoder < self.encoder_low_wrap):
            self.lmult = self.lmult - 1

        self.left = 1.0 * (enc + self.lmult * (self.encoder_max - self.encoder_min))
        self.prev_lencoder = enc

    def rwheelCallback(self, msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_rencoder > self.encoder_high_wrap):
            self.rmult = self.rmult + 1

        if(enc > self.encoder_high_wrap and self.prev_rencoder < self.encoder_low_wrap):
            self.rmult = self.rmult - 1

        self.right = 1.0 * (enc + self.rmult * (self.encoder_max - self.encoder_min))
        self.prev_rencoder = enc

def main(args=None):
    rclpy.init(args=args)
    print("\nDifferential Drive Node Started\n")
    node = DiffTf()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()