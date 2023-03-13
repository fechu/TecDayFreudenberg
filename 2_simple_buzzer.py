import board
import time
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.D7)
led.direction = Direction.OUTPUT

while True:
    led.value = True
    time.sleep(1/800)
    led.value = False
    time.sleep(1/800)
