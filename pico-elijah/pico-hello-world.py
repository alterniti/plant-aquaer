from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)  # Create a pin object for the built-in LED
print ("Blinking LED example")

while True:
    led.value(not led.value())  # Toggle the LED state
    sleep(0.5)  # Wait for 0.5 seconds
# The code above is a simple program that blinks the built-in LED on the Pico board.    
