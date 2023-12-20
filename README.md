# care_taker_robot

### Progress
- Odometery while driving with cmd_vel
- Mapping 


### Packages
- 


### Commands for permissions
- sudo chown robot /dev/gpiomem and sudo chmod g+rw /dev/gpiomem for gpio pins access


### Pin Connections 
Back motors: 
in4 = 17
enb1 = 27
in3 = 22
in1 = 24
in2 = 23
ena1 = 25

Front motors:
in2_4 = 9
enb2 = 10
in2_3 = 11
in2_1 = 7
in2_2 = 8
ena2 = 26

GPIO.output(in1,GPIO.HIGH) #right, back
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.HIGH) #left, back
GPIO.output(in4,GPIO.LOW)
GPIO.output(in2_1,GPIO.HIGH) #right, forward
GPIO.output(in2_2,GPIO.LOW)
GPIO.output(in2_3,GPIO.HIGH) #left, forward
GPIO.output(in2_4,GPIO.LOW)

imu:
gpio 2
gpio 3

### People Counting 
- https://github.com/saimj7/People-Counting-in-Real-Time
- people_counter.py modified
