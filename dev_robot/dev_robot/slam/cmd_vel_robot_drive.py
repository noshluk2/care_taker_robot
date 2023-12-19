import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO


#back
in4 = 17
enb1 = 27
in3 = 22
in1 = 24
in2 = 23
ena1 = 25
#front
in2_4 = 9
enb2 = 10
in2_3 = 11
in2_1 = 7
in2_2 = 8
ena2 = 26
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena1,GPIO.OUT)
GPIO.setup(enb1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

GPIO.setup(in2_1,GPIO.OUT)
GPIO.setup(in2_2,GPIO.OUT)
GPIO.setup(in2_3,GPIO.OUT)
GPIO.setup(in2_4,GPIO.OUT)
GPIO.setup(ena2,GPIO.OUT)
GPIO.setup(enb2,GPIO.OUT)
GPIO.output(in2_1,GPIO.LOW)
GPIO.output(in2_2,GPIO.LOW)
GPIO.output(in2_3,GPIO.LOW)
GPIO.output(in2_4,GPIO.LOW)
p=GPIO.PWM(ena1,1000)
q=GPIO.PWM(enb1,1000)
t=GPIO.PWM(ena2,1000)
u=GPIO.PWM(enb2,1000)

q.start(25)
p.start(25)
t.start(25)
u.start(25)

class FourWheelCmdVelSubscriber(Node):

    def __init__(self):
        super().__init__('four_wheel_cmd_vel_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)


    def listener_callback(self, msg):
        linearx = msg.linear.x
        angularz = msg.angular.z

        if linearx > 0:  # Forward
            self.move_forward()
        elif linearx < 0:  # Backward
            self.move_backward()
        elif angularz > 0:  # Turn Left
            self.turn_left()
        elif angularz < 0:  # Turn Right
            self.turn_right()
        else:  # Stop
            self.stop_motors()

    def move_forward(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(in2_1, GPIO.HIGH)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in2_3, GPIO.HIGH)
        GPIO.output(in2_4, GPIO.LOW)

    def move_backward(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        GPIO.output(in2_1, GPIO.LOW)
        GPIO.output(in2_2, GPIO.HIGH)
        GPIO.output(in2_3, GPIO.LOW)
        GPIO.output(in2_4, GPIO.HIGH)

    def turn_left(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(in2_1, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in2_3, GPIO.HIGH)
        GPIO.output(in2_4, GPIO.LOW)

    def turn_right(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(in2_1, GPIO.HIGH)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in2_3, GPIO.LOW)
        GPIO.output(in2_4, GPIO.LOW)

    def stop_motors(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(in2_1, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in2_3, GPIO.LOW)
        GPIO.output(in2_4, GPIO.LOW)

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_subscriber = FourWheelCmdVelSubscriber()
    rclpy.spin(cmd_vel_subscriber)
    cmd_vel_subscriber.destroy_node()
    GPIO.cleanup()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
