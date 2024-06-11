import RPi.GPIO as GPIO
import time

# Custom imports
from Classes.PCF8574 import PCF8574

# variables
PCF = PCF8574(0x3a)
        

def setup():
    GPIO.setmode(GPIO.BCM)
    PCF.write_byte(0b11111111)
    print(hex(PCF.read_byte()))
    
    GPIO.setup([5, 6, 13, 19], GPIO.OUT)

def main():
    # PCF.write_byte(0b10101010)
    # time.sleep(0.5)
    # PCF.write_byte(0b01010101)
    # time.sleep(0.5)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    time.sleep(1)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    time.sleep(1)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    time.sleep(1)

    # with PCF857(0x38) as pcf:
    #     pcf.write_byte(1)
# At this point, the i2c connection is automatically closed.


def cleanup():
    PCF.close()
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
