import time
from Classes.Button import Button

def default_callback(channel):
    print("Button event detected on channel:", channel)

def setup():
    pass

def main():
    with Button(pin=20, default_callback=default_callback) as button:
        # button.set_press_callback()  # Use default callback for press
        # button.set_release_callback()  # Use default callback for release
        button.set_both_callbacks()  # Use default callback for both press and release

        while True:
            if button.is_pressed:
                print("Button is currently pressed.")
            time.sleep(0.1)

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
