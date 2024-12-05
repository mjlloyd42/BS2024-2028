from machine import PWM, ADC, Pin
import time
import math
import utime
# specifying the pins that the joystick pins and button are connected to
xJS= machine.ADC(27)
yJS= machine.ADC(26)
# line 9 taken from code provided by JC Williams to register the click of the button
swJoy = Pin(16, Pin.IN, Pin.PULL_UP)
swStatus = ""
# specifying where the servomotor pins are connected to on the board, setting the frequency of the PWM pins to 50hz, and setting the duties to 0 to 'reset' them each run, regardless of last state

def servoInitiate(servo):
    servo.freq(50)
    servo.duty_u16(0)
    
servoPin1 = 15
servo1 = machine.PWM(machine.Pin(servoPin1))
servoInitiate(servo1)

servoPin2 = 11
servo2 = machine.PWM(machine.Pin(servoPin2))
servoInitiate(servo2)

servoPin3 = 4
servo3 = machine.PWM(machine.Pin(servoPin3))
servoInitiate(servo3)

while True:
    # reads the value of the joystick position. lines 32-42 are from toptechboy, and was included in the email sent out by JC Williams as a resource: https://toptechboy.com/calibrating-joystick-to-show-positional-angle-in-micropython-on-the-raspberry-pi-pico-w/
    # i would not have been able to figure the math out by myself (at least not within a timely manner), so big thanks to that guy
    xVal=xJS.read_u16()
    yVal=yJS.read_u16()
    
    xVal=int(-.00306*xVal+100.766)
    yVal=int(.00306*yVal-100.766)
    
    mag=math.sqrt(xVal**2+yVal**2)
    if mag<=4:
        xVal=0
        yVal=0
        
# prints out the values of the x and y coordinates of the position of joystick, and also whether the button has been pressed or not
    def swStat():
        if swJoy.value() == 0:
            swStatus = "ON"
        else:
            swStatus = "OFF"
        return (swStatus)
    print(xVal,yVal, "SW:", swStat())

#function servoD1() checks the x-value of the joystick. if over 0, the joystick moves 180 degrees to an a position that will be named 'open'
    # if the value is under 0, the joystick will move back 180 to the initial 'closed' position
    # if the value is 0, the joystick will save the position it is currently in and will not move. 
    def servoD1():
        if xVal > 10:
            smDuty1 = 8191
        elif xVal <-10:
            smDuty1 = 1638
        else:
            smDuty1 = 0
            
        return(smDuty1)
# function servoD2() does the same task as servoD1(), but checks the y values of the joystick instead.
    def servoD2():
        if yVal > 10:
            smDuty2 = 8191
        elif yVal < -10:
            smDuty2 = 1638
        else:
            smDuty2 = 0
        return(smDuty2)
# function servoD3() checks to see if the button is pressed. a pressed button will give swJoy.value() of 0.
# when the value is 0/button is pressed, servo will move to the 180 degree 'open' position, mimicking a claw closing of sorts (we do not have our print)
# when the button is no longer pressed, giving a value 1, it will move back to the 0 degree position, releasing the 'claw'
# unlike servos 1 and 2, this does not save its position. it will either be open at 180 or closed at 0, not a value in between
    def servoD3():
        if swJoy.value() == 0:
            smDuty3 = 8191
        elif swJoy.value() == 1:
            smDuty3 = 1638
        return(smDuty3)
# updates the values of servos 1, 2, and 3 based on the functions above
    servo1.duty_u16(servoD1())
    servo2.duty_u16(servoD2())
    servo3.duty_u16(servoD3())
# delay between checks
    utime.sleep(.1)
