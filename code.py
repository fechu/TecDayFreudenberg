import board
import time
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
