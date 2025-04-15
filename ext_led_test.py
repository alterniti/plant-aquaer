from machine import Pin
from time import sleep


led2=Pin("LED", Pin.OUT)

while True:
    led2.value(not led2.value())
    sleep(0.5)