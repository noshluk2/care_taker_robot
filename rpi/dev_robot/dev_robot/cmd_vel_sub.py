import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO
from geometry_msgs.msg import Twist
in4 = 17
en1 = 27
in3 = 22
in1 = 24
in2 = 23
en = 25
temp1=1
angularz = 0
linearx = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
q=GPIO.PWM(en1,1000)
q.start(25)
p.start(25)
#p is left, q is right

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
	


   
    def listener_callback(self, msg):
        #self.get_logger().info('"%s"' % msg.linear.x)
        linearx = msg.linear.x
        angularz = msg.angular.z
       	if (linearx > 0 and angularz == 0 ):
       		print("Forward: X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.HIGH)
       		GPIO.output(in2,GPIO.LOW)
       		GPIO.output(in3,GPIO.HIGH)
       		GPIO.output(in4,GPIO.LOW)
       	elif (linearx < 0 and angularz == 0 ):
       		print("Backward: X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.LOW)
       		GPIO.output(in2,GPIO.HIGH)
       		GPIO.output(in3,GPIO.LOW)
       		GPIO.output(in4,GPIO.HIGH)
       	elif (linearx == 0 and angularz > 0 ):
       		print("Turn Left X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.LOW)
       		GPIO.output(in2,GPIO.HIGH)
       		GPIO.output(in3,GPIO.HIGH)
       		GPIO.output(in4,GPIO.LOW)
       	elif (linearx == 0 and angularz < 0 ):
       		print("Turn Right X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.HIGH)
       		GPIO.output(in2,GPIO.LOW)
       		GPIO.output(in3,GPIO.LOW)
       		GPIO.output(in4,GPIO.HIGH)
       	elif (linearx > 0 and angularz < 0 ):
       		print("Move Forward, Tilt Right X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.HIGH)
       		GPIO.output(in2,GPIO.LOW)
       		GPIO.output(in3,GPIO.HIGH)
       		GPIO.output(in4,GPIO.LOW)
       		p.ChangeDutyCycle(50)
        	q.ChangeDutyCycle(30)
       	elif (linearx > 0 and angularz > 0 ):
       		print("Move Forward, Tilt Left X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.HIGH)
       		GPIO.output(in2,GPIO.LOW)
       		GPIO.output(in3,GPIO.HIGH)
       		GPIO.output(in4,GPIO.LOW)
       		p.ChangeDutyCycle(30)
        	q.ChangeDutyCycle(50)
       	elif (linearx < 0 and angularz < 0 ):
       		print("Move Backward, Tilt Left X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.LOW)
       		GPIO.output(in2,GPIO.HIGH)
       		GPIO.output(in3,GPIO.LOW)
       		GPIO.output(in4,GPIO.HIGH)
       		p.ChangeDutyCycle(30)
        	q.ChangeDutyCycle(50)
       	elif (linearx < 0 and angularz > 0 ):
       		print("Move Backward, Tilt Right X="+ str(linearx) + "Z=" + str(angularz))
       		GPIO.output(in1,GPIO.LOW)
       		GPIO.output(in2,GPIO.HIGH)
       		GPIO.output(in3,GPIO.LOW)
       		GPIO.output(in4,GPIO.HIGH)
       		p.ChangeDutyCycle(50)
        	q.ChangeDutyCycle(30)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    	
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()