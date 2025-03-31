#use pi2 for this one 
from machine import Pin
from time import sleep

# Motor Pins
motor1 = Pin(16, Pin.OUT) # IN1 

# Motor Funtions
def motor_on():
    motor1.value(1) # Turn on the motor by setting IN1 high
    print("Motor is ON") 
    