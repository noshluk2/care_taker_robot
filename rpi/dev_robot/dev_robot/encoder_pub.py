import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import RPi.GPIO as GPIO

class EncoderPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')
        self.publisher = self.create_publisher(Int32, 'encoder_value', 10)
        self.timer = self.create_timer(1, self.publish_encoder_value)  # Publish every 0.1 seconds

        # Encoder setup
        self.frontleft_b = 4
        self.frontleft_a = 18
        self.frontright_a = 13
        self.frontright_b = 19
        self.backleft_b = 5
        self.backleft_a = 6
        self.backright_a = 16 #A pin
        self.backright_b = 20 #B pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.frontright_a, GPIO.IN)
        GPIO.setup(self.frontright_b, GPIO.IN)
        GPIO.setup(self.backright_a, GPIO.IN)
        GPIO.setup(self.backright_b , GPIO.IN)
        GPIO.setup(self.backleft_a, GPIO.IN)
        GPIO.setup(self.backleft_b , GPIO.IN)
        GPIO.setup(self.frontleft_a, GPIO.IN)
        GPIO.setup(self.frontleft_b , GPIO.IN)
        self.outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        FRlast_AB = 0b00
        FLlast_AB = 0b00
        BRlast_AB = 0b00
        BLlast_AB = 0b00
        self.FRcounter = 0
        FLcounter = 0
        BRcounter = 0
        BLcounter = 0
        FRcurrent_AB = 0
        self.FRlast_AB = 0

    def publish_encoder_value(self):
        FRA = GPIO.input(self.frontright_a)
        FRB = GPIO.input(self.frontright_b)
        FRcurrent_AB = (FRA << 1) | FRB
        position = (self.FRlast_AB << 2) | FRcurrent_AB
        if((self.FRcounter - self.outcome[position]) > self.FRcounter):
                    print("Robot is Moving Forwards and the FR Counter is " + str(self.FRcounter))
        elif ((self.FRcounter - self.outcome[position]) < self.FRcounter):
                print("Robot is Moving Backwards and the FR Counter is " + str(self.FRcounter))       
        msg = Int32()
        msg.data = self.FRcounter
        self.FRcounter = self.FRcounter - self.outcome[position]
        self.FRlast_AB = FRcurrent_AB
        self.publisher.publish(msg)
        """FRA = GPIO.input(self.frontright_a)
        FRB = GPIO.input(self.frontright_b)
        #print("FRA and FRB is " + str(FRA) +" & "+ str(FRB))
        FRcurrent_AB = (FRA << 1) | FRB
        #print("FRcurrent_AB is " + str(FRcurrent_AB))
        position = (self.FRlast_AB << 2) | FRcurrent_AB
        #print("FRcurrent and FRLast is " + str(FRcurrent_AB) + " - " + str(self.FRlast_AB))
        print("FRPosition is " + str(self.outcome[position]))
        if((self.FRcounter - self.outcome[position]) > self.FRcounter):
                print("Robot is Moving Forwards and the FR Counter is " + str(self.FRcounter))
        elif ((self.FRcounter - self.outcome[position]) < self.FRcounter):
            print("Robot is Moving Backwards and the FR Counter is " + str(self.FRcounter))
        # Publish the counter value
        msg = Int32()
        self.FRcounter = self.FRcounter - self.outcome[position]
        msg.data = self.FRcounter
        self.FRlast_AB = FRcurrent_AB
        self.publisher.publish(msg)"""

def main(args=None):
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    encoder_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
