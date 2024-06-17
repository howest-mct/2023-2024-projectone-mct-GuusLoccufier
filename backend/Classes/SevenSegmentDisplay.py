import RPi.GPIO as GPIO
import time
import threading
from Classes.PCF8574 import PCF8574

class SevenSegmentDisplay:
    # Map of digits to segments (abcdefg)
    digit_to_segments = {
        '0': 0b00111111,
        '1': 0b00000110,
        '2': 0b01011011,
        '3': 0b01001111,
        '4': 0b01100110,
        '5': 0b01101101,
        '6': 0b01111101,
        '7': 0b00000111,
        '8': 0b01111111,
        '9': 0b01101111,
        '-': 0b01000000,
        ' ': 0b00000000
    }

    def __init__(self, pcf8574_address=0x38, i2c_bus=1, digit_pins=[5, 6, 13, 19], refresh_rate=0.005):
        self.pcf = PCF8574(pcf8574_address, i2c_bus)
        self.digit_pins = digit_pins
        self.refresh_rate = refresh_rate
        self.current_number = '    '

        GPIO.setmode(GPIO.BCM)
        for pin in self.digit_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

        self.update_thread = None
        self.running = False

    def display_number(self, number):
        self.current_number = f'{number:4}'[-4:]  # Ensure it's 4 characters long
        if not self.running:
            self.running = True
            self.update_thread = threading.Thread(target=self._update_display)
            self.update_thread.start()

    def _update_display(self):
        while self.running:
            for i in range(4):
                self.pcf.write_byte(self.digit_to_segments.get(self.current_number[i], 0))
                GPIO.output(self.digit_pins[i], GPIO.LOW)
                time.sleep(self.refresh_rate)
                GPIO.output(self.digit_pins[i], GPIO.HIGH)

    def stop(self):
        self.running = False
        if self.update_thread:
            self.update_thread.join()

    def cleanup(self):
        self.stop()
        self.pcf.close()
        GPIO.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
