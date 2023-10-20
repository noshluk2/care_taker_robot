import RPi.GPIO as GPIO
frontleft_b = 4
frontleft_a = 18
frontright_a = 13
frontright_b = 19
backleft_b = 5
backleft_a = 6
backright_a = 16 #A pin
backright_b = 20 #B pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(frontright_a, GPIO.IN)
GPIO.setup(frontright_b , GPIO.IN)
GPIO.setup(backright_a, GPIO.IN)
GPIO.setup(backright_b , GPIO.IN)
GPIO.setup(backleft_a, GPIO.IN)
GPIO.setup(backleft_b , GPIO.IN)
GPIO.setup(frontleft_a, GPIO.IN)
GPIO.setup(frontleft_b , GPIO.IN)

outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
FRlast_AB = 0b00
FLlast_AB = 0b00
BRlast_AB = 0b00
BLlast_AB = 0b00
FRcounter = 0
FLcounter = 0
BRcounter = 0
BLcounter = 0

while True:
    FRA = GPIO.input(frontright_a)
    FRB = GPIO.input(frontright_b)
    FRcurrent_AB = (FRA << 1) | FRB
    position = (FRlast_AB << 2) | FRcurrent_AB
    #print("FRcurrent and FRLast is " + str(FRcurrent_AB) + " - " + str(FRlast_AB))
    print("FRPosition is " + str(outcome[position]))
    if((FRcounter - outcome[position]) > FRcounter):
                print("Robot is Moving Forwards and the FR Counter is " + str(FRcounter))
    elif ((FRcounter - outcome[position]) < FRcounter):
            print("Robot is Moving Backwards and the FR Counter is " + str(FRcounter))
    FRcounter = FRcounter - outcome[position]
    FRlast_AB = FRcurrent_AB

    FLA = GPIO.input(frontleft_a)
    FLB = GPIO.input(frontleft_b)
    FLcurrent_AB = (FLA << 1) | FLB
    position = (FLlast_AB << 2) | FLcurrent_AB
    if((FLcounter - outcome[position]) > FLcounter):
                print("Robot is Moving Forwards and the FL Counter is " + str(FLcounter))
    elif ((FLcounter - outcome[position]) < FLcounter):
            print("Robot is Moving Backwards and the FL Counter is " + str(FLcounter))
    FLcounter = FLcounter - outcome[position]
    FLlast_AB = FLcurrent_AB

    BRA = GPIO.input(backright_a)
    BRB = GPIO.input(backright_b)
    BRcurrent_AB = (BRA << 1) | BRB
    position = (BRlast_AB << 2) | BRcurrent_AB
    if((BRcounter - outcome[position]) > BRcounter):
                print("Robot is Moving Forwards and the BR Counter is " + str(BRcounter))
    elif ((BRcounter - outcome[position]) < BRcounter):
            print("Robot is Moving Backwards and the FR Counter is " + str(BRcounter))
    BRcounter = BRcounter - outcome[position]
    BRlast_AB = BRcurrent_AB

    BLA = GPIO.input(backleft_a)
    BLB = GPIO.input(backleft_b)
    BLcurrent_AB = (BLA << 1) | BLB
    position = (BLlast_AB << 2) | BLcurrent_AB
    if((BLcounter - outcome[position]) > BLcounter):
                print("Robot is Moving Forwards and the BL Counter is " + str(BLcounter))
    elif ((BLcounter - outcome[position]) < BLcounter):
            print("Robot is Moving Backwards and the BL Counter is " + str(BLcounter))
    BLcounter = BLcounter - outcome[position]
    BLlast_AB = BLcurrent_AB

    #print(A)    
    #print(B)
