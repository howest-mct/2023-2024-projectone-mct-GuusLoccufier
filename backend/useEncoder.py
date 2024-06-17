import RPi.GPIO as GPIO
import time

# Custom imports
from Classes.Encoder import Encoder

# variables
encoder = Encoder(clk=24, dt=23, sw=25)

def setup():
    GPIO.setmode(GPIO.BCM)

def main():
    if encoder.pressed():
        print("Switch pressed")
    rotation_value = encoder.value()
    if rotation_value != 0:
        print(f"Rotation value: {rotation_value}")

    # with Encoder(clk=24, dt=23, sw=25) as enc:
    #     if enc.pressed():
    #         print("Switch pressed")
    #     rotation_value = enc.value()
    #     if rotation_value != 0:
    #         print(f"Rotation value: {rotation_value}")

def cleanup():
    encoder.close()
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
