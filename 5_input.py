import board
import simpleio
from digitalio import DigitalInOut, Direction
import time

input = DigitalInOut(board.D0)
input.direction = Direction.INPUT

while True:
    if input.value == False:
        simpleio.tone(board.D7, 400, duration=0.3)
    time.sleep(0.1)
