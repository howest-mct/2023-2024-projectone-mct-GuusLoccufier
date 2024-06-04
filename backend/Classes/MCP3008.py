import spidev

#            MCP3008
#           +--- ---+
# CH0  Pin 1|o  '   | Pin 16  VCC
# CH1  Pin 2|       | Pin 15  VREF
# CH2  Pin 3|       | Pin 14  AGND
# CH3  Pin 4|       | Pin 13  CLK
# CH4  Pin 5|       | Pin 12  MISO
# CH5  Pin 6|       | Pin 11  MOSI
# CH6  Pin 7|       | Pin 10  CS/SHDN
# CH7  Pin 8|       | Pin 9   GND
#           +-------+

class MCP3008:
    """
    A class for interfacing with the MCP3008 ADC using SPI.
    """

    def __init__(self, bus=0, device=0, max_speed_hz=100000):
        """
        Initialize the MCP3008 object.

        :param bus: SPI bus number.
        :param device: SPI device number.
        :param max_speed_hz: Maximum SPI speed in Hz.
        """
        self.bus = bus
        self.device = device
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz

    def read_channel(self, channel):
        """
        Read the analog value from the specified channel.

        :param channel: Channel number (0-7).
        :return: Analog value (0-1023).
        """
        if not 0 <= channel <= 7:
            raise ValueError("Channel must be between 0 and 7.")
        
        bytes_out = [0x01, (0x8 | channel) << 4, 0x00]
        bytes_in = self.spi.xfer2(bytes_out)
        value = ((bytes_in[1] & 0x03) << 8) | bytes_in[2]
        return value

    def close(self):
        """
        Close the SPI connection.
        """
        self.spi.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
