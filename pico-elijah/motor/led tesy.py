from machine import Pin
from time import sleep

led = Pin('3V3(OUT)', Pin.OUT)  # Create a pin object for the LED in output mode

led.value(1)  # Turn the LED on