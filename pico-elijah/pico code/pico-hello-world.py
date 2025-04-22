from machine import Pin # type: ignore
from time import sleep

pin = Pin("LED", Pin.OUT)

while True:
    try:
        pin.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")
