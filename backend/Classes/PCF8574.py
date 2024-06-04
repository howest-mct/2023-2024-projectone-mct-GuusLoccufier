from smbus import SMBus
import RPi.GPIO as GPIO

#            MCP3008
#           +--- ---+
# A0   Pin 1|o  '   | Pin 16  VCC
# A1   Pin 2|       | Pin 15  SDA
# A2   Pin 3|       | Pin 14  SCL
# P0   Pin 4|       | Pin 13  _INT
# P1   Pin 5|       | Pin 12  P7
# P2   Pin 6|       | Pin 11  P6
# P3   Pin 7|       | Pin 10  P5
# GND  Pin 8|       | Pin 9   P4
#           +-------+

class PCF8574:
    """
    A class for interfacing with the PCF8574 GPIO expander using SMBus.
    """

    def __init__(self, address, bus=1, interrupt_pin=None):
        """
        Initialize the PCF8574 object.

        :param address: I2C address of the PCF8574.
        :param bus: I2C bus number.
        :param interrupt_pin: GPIO pin number for interrupt (optional).
        """
        self.address = address
        self.bus = bus
        self.interrupt_pin = interrupt_pin
        self.i2c = SMBus(bus)
        if interrupt_pin is not None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(interrupt_pin, GPIO.IN)
            GPIO.add_event_detect(interrupt_pin, GPIO.FALLING, callback=self.handle_interrupt)

    def write_byte(self, value):
        """
        Write a byte value to the PCF8574.

        :param value: Byte value to write.
        """
        self.i2c.write_byte(self.address, value)

    def read_byte(self):
        """
        Read a byte value from the PCF8574.

        :return: Byte value read from the PCF8574.
        """
        return self.i2c.read_byte(self.address)

    def handle_interrupt(self, channel):
        """
        Handle the interrupt by reading a byte from the PCF8574.

        :param channel: The GPIO channel that triggered the interrupt.
        """
        value = self.read_byte()
        print(f"Interrupt detected on channel {channel}: value read = {value}")

    def close(self):
        """
        Close the SMBus connection and clean up GPIO if interrupt pin is defined.
        """
        self.i2c.close()
        if self.interrupt_pin is not None:
            GPIO.remove_event_detect(self.interrupt_pin)
            GPIO.cleanup(self.interrupt_pin)

    def __enter__(self):
        """
        Enter the context manager. Returns itself.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager. Closes the SMBus connection.
        """
        self.close()
