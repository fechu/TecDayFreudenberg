"""
Description: 
    Plays a tone on the buzzer if the connected sensor value reads False

Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7

    Sensor Vcc -> 3V3
    Sensor Gnd -> GND
    Sensor S   -> D9

Additional Challenges:
    - Play a melody when the sensor activates
    - USe multiple sensors and do different actions for each of them
"""
import board
import simpleio
from digitalio import DigitalInOut, Direction
import time

# Set the D9 pin up to read from the sensor
input = DigitalInOut(board.D9)
input.direction = Direction.INPUT

while True:
    # If the sensor is activated, play a short tone on the buzzer
    if input.value == False:
        simpleio.tone(board.D7, 400, duration=0.3)
    time.sleep(0.1)
