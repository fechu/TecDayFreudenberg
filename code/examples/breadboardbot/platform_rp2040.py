import adafruit_dht
import adafruit_hcsr04
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_motor import servo
import board
import busio
from digitalio import DigitalInOut, Direction
import keypad
import neopixel
import pwmio
import time


class Robot:
    """Primary Xiao RP2040-based BreadboardBot platform definition."""

    def __init__(self, line_sensors=True, sonar=False, dht11=False, i2c=False, uart=False, motor_right_pin=board.D6):
        self.led = DigitalInOut(board.LED_GREEN)
        self.led.direction = Direction.OUTPUT
        self.keys = keypad.Keys((board.D1,), value_when_pressed=False, pull=True)
        self.motor_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
        self.motor_right = servo.ContinuousServo(pwmio.PWMOut(motor_right_pin, frequency=50))
        if line_sensors:
            self.line_left = DigitalInOut(board.D10)
            self.line_right = DigitalInOut(board.D7)
        if sonar:
            self.sonar = adafruit_hcsr04.HCSR04(
                trigger_pin=board.D4, echo_pin=board.D3, timeout=0.05
            )
        if dht11:
            self.dht11 = adafruit_dht.DHT11(board.D8)
        if uart:
            self.uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.1)
        if i2c:
            # SDA=D4, SCL=D5
            self.i2c = board.I2C()
        self.rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
        self.rainbow = Rainbow(self.rgb_pixel, speed=0.1, period=2)
        self.last_sonar_measurement_time = -1
        self.last_sonar_measurement = None
        self.buzzer_pin = board.D9
        self.buzzer_pwm = pwmio.PWMOut(
            self.buzzer_pin, frequency=1000, variable_frequency=True
        )
        self.buzzer_off_time = None
        self.led_off_time = None
        self.now = time.monotonic()

        # Welcome triple-blink / beep
        for i in range(3):
            self.blink()
            self.beep()
            self.sleep(0.1)

    def update(self):
        self.now = time.monotonic()
        if self.buzzer_off_time and self.now >= self.buzzer_off_time:
            self.buzzer_pwm.duty_cycle = 0
            self.buzzer_off_time = None
        if self.led_off_time and self.now >= self.led_off_time:
            self.led.value = True
            self.led_off_time = None

    def play_melody(self, melody):
        """Plays melody (blocking)."""
        for note, duration in melody:
            if note > 0:
                self.beep(int(note))
            self.sleep(duration)

    def beep(self, frequency=1000):
        self.buzzer_pwm.frequency = frequency
        self.buzzer_pwm.duty_cycle = 2**15
        self.buzzer_off_time = self.now + 0.05

    def blink(self):
        self.led.value = True
        self.led_off_time = self.now + 0.05

    def sleep(self, duration):
        now = self.now
        while self.now < now + duration:
            self.update()

    def drive(self, left_throttle, right_throttle):
        # Every cheap servo is a unique snowflake and if you want to get
        # better precision, you might want to calibrate the constants used
        # here until calling drive(0, 0) consistently results in fully stopped
        # motors
        self.motor_left.throttle = 0.13 * left_throttle - 0.07
        self.motor_right.throttle = -0.11 * right_throttle

    def get_sonar_distance(self):
        if (
            self.last_sonar_measurement is None
            or (self.now - self.last_sonar_measurement_time) > 0.1
        ):
            self.last_sonar_measurement_time = self.now
            try:
                self.last_sonar_measurement = self.sonar.distance
            except RuntimeError:
                # Do not crash on errors from sonar, which sometimes happen
                self.last_sonar_measurement = None
        return self.last_sonar_measurement

    def loop_forever(self, behaviors):
        while True:
            self.update()
            for b in behaviors:
                b(self)
