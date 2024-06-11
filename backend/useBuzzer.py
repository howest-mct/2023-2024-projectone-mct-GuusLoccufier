import time
from Classes.Buzzer import Buzzer

buzzer = Buzzer(12)

def setup():
    pass

def main():
    # with Buzzer(pin=12) as buzzer:
    buzzer.beep(frequency=1000, duration=1)
    time.sleep(1)
    buzzer.beep(frequency=1500, duration=1)
    time.sleep(1)
    buzzer.beep(frequency=2000, duration=1)
    time.sleep(1)
    buzzer.buzz_on(frequency=2500)
    time.sleep(1)
    buzzer.buzz_off()

def cleanup():
    buzzer.cleanup()

if __name__ == "__main__":
    print("Starting program")
    start_time = time.time()
    setup()
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print(f"Stopping program --- ran for: {time.time() - start_time} seconds")
