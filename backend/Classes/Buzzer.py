import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=12):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.pin, 1000)  # Set frequency to 1kHz

    def buzz_on(self, frequency=1000):
        self.buzzer.ChangeFrequency(frequency)
        self.buzzer.start(50)  # 50% duty cycle

    def buzz_off(self):
        self.buzzer.stop()

    def beep(self, frequency=1000, duration=1):
        self.buzz_on(frequency)
        time.sleep(duration)
        self.buzz_off()

    def cleanup(self):
        self.buzz_off()
        GPIO.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
