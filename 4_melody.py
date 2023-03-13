import board
import simpleio
import time

melody = [400, 800, 400, 800]
while True:
    for note in melody:
        simpleio.tone(board.D7, note, duration=0.3)
    time.sleep(1.0)
