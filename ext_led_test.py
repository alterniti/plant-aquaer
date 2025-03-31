from machine import Pin
from time import sleep

print("hello?")
led=Pin(8, Pin.OUT)
led2=Pin("LED", Pin.OUT)


# led.value(not led.value())
# led2.value(not led.value())
# sleep(0.5)
# print(led.value)