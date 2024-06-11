import time
from Classes.OLEDDisplay import OLEDDisplay

def setup():
    pass

def main():
    with OLEDDisplay() as display:
        display.clear_display()
        time.sleep(1)
        display.write_text("Hello, world!\n192.168.192.143")
        time.sleep(5)
        display.write_text("Testing!")
        time.sleep(5)

if __name__ == "__main__":
    print("Starting program")
    start_time = time.time()
    setup()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        pass
    finally:
        print(f"Stopping program --- ran for: {time.time() - start_time} seconds")
