import RPi.GPIO as GPIO
A_pin = 16
B_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB= 0b00
counter = 0

while True:

    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A << 1) | B
    position = (last_AB << 2) | current_AB
    if((counter - outcome[position]) > counter):
                print("Robot is Moving Forwards and the Counter is " + str(counter))
    elif ((counter - outcome[position]) < counter):
            print("Robot is Moving Backwards and the Counter is " + str(counter))
    counter = counter - outcome[position]
    last_AB = current_AB

    #print(A)    
    #print(B)