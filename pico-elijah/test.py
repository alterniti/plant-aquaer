from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT) #create a pin object
print ("Blinking LED example")

while True:
    led.value(not led.value()) #toggle the LEd
    sleep(0.5) #sleep for 1 second