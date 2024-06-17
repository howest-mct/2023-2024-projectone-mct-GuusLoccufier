import RPi.GPIO as GPIO

class Encoder:
    """
    A class to interface with a rotary encoder with switch.

    Attributes:
        clk (int): The GPIO pin number for the clock signal.
        dt (int): The GPIO pin number for the data signal.
        sw (int): The GPIO pin number for the switch signal.
        clk_state_prev (bool): The previous state of the clock signal.
        counter (int): The counter to track encoder turns.
        switch_pressed (bool): Flag to indicate if the switch was pressed.
    """

    def __init__(self, clk, dt, sw):
        """
        Initialize the Encoder object.

        :param clk: GPIO pin number for the clock signal.
        :param dt: GPIO pin number for the data signal.
        :param sw: GPIO pin number for the switch signal.
        """

        GPIO.setmode(GPIO.BCM)

        GPIO.setup((dt, clk, sw), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(clk, GPIO.BOTH, self.decode_rotation, bouncetime=1)
        GPIO.add_event_detect(sw, GPIO.FALLING, self.callback, bouncetime=200)

        self.dt = dt
        self.clk = clk
        self.sw = sw
        self.clk_state_prev = GPIO.input(clk)
        self.counter = 0
        self.switch_pressed = False

    def decode_rotation(self, pin):
        """
        Decode the rotation of the encoder.

        :param pin: GPIO pin that triggered the event.
        """
        dt_state = GPIO.input(self.dt)
        clk_state = GPIO.input(self.clk)

        if clk_state != self.clk_state_prev and not clk_state:
            if dt_state != clk_state:
                self.counter += 1
            else:
                self.counter -= 1
        self.clk_state_prev = clk_state

    def callback(self, pin):
        """
        Callback function for the switch press.

        :param pin: GPIO pin that triggered the event.
        """
        if pin == self.sw:
            self.switch_pressed = True

    def value(self):
        """
        Get the current value of the encoder.

        :return: The encoder count value since last checked.
        """
        value = self.counter
        self.counter = 0
        return value

    def pressed(self):
        """
        Check if the switch was pressed since the last check.

        :return: True if the switch was pressed, False otherwise.
        """
        if self.switch_pressed:
            self.switch_pressed = False
            return True
        return False

    def close(self):
        """
        Clean up GPIO resources.
        """
        GPIO.remove_event_detect(self.clk)
        GPIO.remove_event_detect(self.sw)
        GPIO.cleanup([self.clk, self.dt, self.sw])

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
