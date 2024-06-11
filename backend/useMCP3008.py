import RPi.GPIO as GPIO
import time

# Custom imports
from Classes.MCP3008 import MCP3008

# variables
MCP = MCP3008(0, 0)

def setup():
    GPIO.setmode(GPIO.BCM)

def main():
    piezoelectric = MCP.read_channel(0x00)
    if piezoelectric > 50:
        print(f"Piezzo => {piezoelectric}")

    # with MCP3008(0, 0) as mcp:
    #     value = mcp.read_channel(0)
    #     print("Analog value:", value)
# At this point, the SPI connection is automatically closed.


def cleanup():
    MCP.close()
    GPIO.cleanup()

if __name__ == '__main__':
    print("Starting program")
    start_time = time.time()
    setup()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        print(f"Stopping program --- ran for: {time.time() - start_time} seconds")
