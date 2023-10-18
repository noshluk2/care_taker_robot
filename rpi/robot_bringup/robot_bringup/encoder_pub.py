import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import RPi.GPIO as GPIO

class EncoderPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')
        self.publisher = self.create_publisher(Int32, 'encoder_value', 10)
        self.timer = self.create_timer(0.1, self.publish_encoder_value)  # Publish every 0.1 seconds

        # Encoder setup
        self.A_pin = 16
        self.B_pin = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A_pin, GPIO.IN)
        GPIO.setup(self.B_pin, GPIO.IN)
        self.outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        self.last_AB = 0b00
        self.counter = 0

    def publish_encoder_value(self):
        A = GPIO.input(self.A_pin)
        B = GPIO.input(self.B_pin)
        current_AB = (A << 1) | B
        position = (self.last_AB << 2) | current_AB
        change = self.outcome[position]
        if change:
            self.counter += change
        self.last_AB = current_AB

        # Publish the counter value
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    encoder_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
