import time
from Classes.OLEDDisplay import OLEDDisplay

display = OLEDDisplay()

def setup():
    pass

def main():
    display.write_text("Hello, world!\n192")
    display.write_text("Hello, world!\n192.168")
    display.write_text("Hello, world!\n192.168.88")
    display.write_text("Hello, world!\n192.168.88.143")

def cleanup():
    display.close()

if __name__ == "__main__":
    print("Starting program")
    start_time = time.time()
    setup()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        cleanup()
    finally:
        print(f"Stopping program --- ran for: {time.time() - start_time} seconds")
