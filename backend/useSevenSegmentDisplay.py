import time
from Classes.SevenSegmentDisplay import SevenSegmentDisplay

display = SevenSegmentDisplay(0x3a)

def setup():
    pass

def main():
    # with SevenSegmentDisplay(0x3a) as display:
    for i in range(10000):
        print(i)
        display.display_number(i)
        time.sleep(0.2)
        # stop the display update if needed
        if i == 9999:
            display.stop()

def cleanup():
    display.cleanup()

if __name__ == "__main__":
    print("Starting program")
    start_time = time.time()
    setup()
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
    finally:
        print(f"Stopping program --- ran for: {time.time() - start_time} seconds")
