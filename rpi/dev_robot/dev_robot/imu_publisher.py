import time
import board
import adafruit_mpu6050
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

class ImuPublisher(Node):

    def __init__(self):
        super().__init__('imu_publisher')
        self.publisher_ = self.create_publisher(String, 'imu_value', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        i2c = board.I2C()  # uses board.SCL and board.SDA
        mpu = adafruit_mpu6050.MPU6050(i2c)

    def timer_callback(self):
        msg = String()
        msg.data = '%.2f,%.2f,%.2f' % (mpu.acceleration)
        self.publisher_.publish(msg)
        self.get_logger().info('IMU x,y,z: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()