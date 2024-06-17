from RPi import GPIO

class Button:
    def __init__(self, pin, default_callback=None, debounce_time=200):
        """
        Initialize the Button object.

        :param pin: GPIO pin number for the button.
        :param default_callback: Default function to call when the button is pressed or released.
        :param debounce_time: Debounce time in milliseconds for debouncing the button press.
        """
        self.pin = pin
        self.default_callback = default_callback
        self.debounce_time = debounce_time

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def is_pressed(self):
        """
        Check if the button is currently pressed.

        :return: True if the button is pressed, False otherwise.
        """
        return not GPIO.input(self.pin)

    def set_press_callback(self, callback=None):
        """
        Set the callback function for the button press event.

        :param callback: Function to call when the button is pressed.
        """
        if callback is None:
            callback = self.default_callback
        if callback is not None:
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=callback, bouncetime=self.debounce_time)

    def set_release_callback(self, callback=None):
        """
        Set the callback function for the button release event.

        :param callback: Function to call when the button is released.
        """
        if callback is None:
            callback = self.default_callback
        if callback is not None:
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback=callback, bouncetime=self.debounce_time)

    def set_both_callbacks(self, callback=None):
        """
        Set the callback function for both button press and release events.

        :param callback: Function to call when the button is pressed or released.
        """
        if callback is None:
            callback = self.default_callback
        if callback is not None:
            GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=callback, bouncetime=self.debounce_time)

    def close(self):
        """
        Clean up GPIO resources.
        """
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)

    def __enter__(self):
        """
        Enter the context manager. Returns itself.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager. Cleans up GPIO resources.
        """
        self.close()
