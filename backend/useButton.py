import time
from Classes.Button import Button

def default_callback(channel):
    print("Button event detected on channel:", channel)

b1 = Button(20, default_callback)
b2 = Button(21, default_callback)

def setup():
    pass

def main():
        b1.set_press_callback()  # Use default callback for press
        b2.set_press_callback()  # Use default callback for press
        # button.set_release_callback()  # Use default callback for release
        # button.set_both_callbacks()  # Use default callback for both press and release

        while True:
            if b1.is_pressed:
                print("Button 20 is currently pressed.")
            if b2.is_pressed:
                print("Button 21 is currently pressed.")
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
