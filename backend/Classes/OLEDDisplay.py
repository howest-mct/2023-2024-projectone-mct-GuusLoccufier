import time
import os
import threading
import textwrap
from PIL import Image, ImageDraw, ImageFont
import smbus

class OLEDDisplay:
    """
    A class to interface with an OLED display via I2C.

    Attributes:
        i2c_bus (int): The I2C bus number.
        i2c_address (int): The I2C address of the OLED display.
        width (int): The width of the OLED display.
        height (int): The height of the OLED display.
        pages (int): The number of pages in the OLED display (height divided by 8).
    """
    def __init__(self, i2c_bus=1, i2c_address=0x3C):
        """
        Initialize the OLEDDisplay object.

        :param i2c_bus: The I2C bus number.
        :param i2c_address: The I2C address of the OLED display.
        """
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.bus = smbus.SMBus(self.i2c_bus)

        self.width = 128
        self.height = 64
        self.pages = self.height // 8

        self.init_display()

    def init_display(self):
        """
        Initialize the OLED display with a series of commands.
        """
        commands = [
            0xAE,  # Display off
            0xD5, 0x80,  # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F,  # Set multiplex ratio(1 to 64)
            0xD3, 0x00,  # Set display offset. 00 = no offset
            0x40,  # Set start line address
            0x8D, 0x14,  # Charge Pump Setting
            0x20, 0x00,  # Memory Mode
            0xA1,  # Set Segment Re-map. A0=address mapped; A1=address 127 mapped.
            0xC8,  # Set COM Output Scan Direction
            0xDA, 0x12,  # Set COM Pins hardware configuration
            0x81, 0xCF,  # Set contrast control register
            0xD9, 0xF1,  # Set pre-charge period
            0xDB, 0x40,  # Set VCOMH Deselect Level
            0xA4,  # Entire Display ON; A4=Follow RAM content; A5=Ignore RAM content
            0xA6,  # Set Normal Display. A6=Normal; A7=Inverse
            0x2E,  # Deactivate scroll
            0xAF   # Display ON
        ]

        for cmd in commands:
            self.write_command(cmd)

    def write_command(self, cmd):
        """
        Write a command to the OLED display.

        :param cmd: The command byte to write.
        """
        self.bus.write_byte_data(self.i2c_address, 0x00, cmd)

    def write_data(self, data):
        """
        Write data to the OLED display.

        :param data: A list of data bytes to write.
        """
        for i in range(0, len(data), 32):
            self.bus.write_i2c_block_data(self.i2c_address, 0x40, data[i:i+32])

    def display_image(self, image_path):
        """
        Display an image on the OLED display.

        :param image_path: The path to the image file.
        """
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found.")
            return

        image = Image.open(image_path).convert('1').resize((self.width, self.height), Image.LANCZOS)
        pixel_data = list(image.getdata())
        pages = [0x00] * (self.width * self.pages)

        for i in range(self.height):
            for j in range(self.width):
                if pixel_data[i * self.width + j]:
                    pages[j + (i // 8) * self.width] |= (1 << (i % 8))

        self.write_command(0x22)
        self.write_command(0x00)
        self.write_command(0x07)
        self.write_command(0x21)
        self.write_command(0x00)
        self.write_command(0x7F)

        for page in range(self.pages):
            self.write_command(0xB0 + page)
            self.write_command(0x00)
            self.write_command(0x10)
            self.write_data(pages[page * self.width:(page + 1) * self.width])

    def write_text(self, text, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size=10):
        """
        Display text on the OLED display.

        :param text: The text to display.
        :param font_path: The path to the TTF font file.
        :param font_size: The font size.
        """
        image = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        max_width = self.width
        lines = textwrap.wrap(text, width=int(max_width / (font_size * 0.6)))

        y = 0
        for line in lines:
            draw.text((1, y), line, font=font, fill=255)
            y += (font_size + 1)

        pixel_data = list(image.getdata())
        pages = [0x00] * (self.width * self.pages)

        for i in range(self.height):
            for j in range(self.width):
                if pixel_data[i * self.width + j]:
                    pages[j + (i // 8) * self.width] |= (1 << (i % 8))

        self.write_command(0x22)
        self.write_command(0x00)
        self.write_command(0x07)
        self.write_command(0x21)
        self.write_command(0x00)
        self.write_command(0x7F)

        for page in range(self.pages):
            self.write_command(0xB0 + page)
            self.write_command(0x00)
            self.write_command(0x10)
            self.write_data(pages[page * self.width:(page + 1) * self.width])

    def clear_display(self):
        """
        Clear the OLED display.
        """
        self.write_command(0x22)
        self.write_command(0x00)
        self.write_command(0x07)
        self.write_command(0x21)
        self.write_command(0x00)
        self.write_command(0x7F)

        pages = [0x00] * (self.width * self.pages)
        for page in range(self.pages):
            self.write_command(0xB0 + page)
            self.write_command(0x00)
            self.write_command(0x10)
            self.write_data(pages[page * self.width:(page + 1) * self.width])

    def display_image_thread(self, image_path, duration):
        """
        Display an image on the OLED display for a specified duration in a separate thread.

        :param image_path: The path to the image file.
        :param duration: The duration to display the image in seconds.
        """
        def display_image_thread_worker():
            self.display_image(image_path)
            time.sleep(duration)
            self.clear_display()

        thread = threading.Thread(target=display_image_thread_worker)
        thread.start()

    def display_menu(self, menu_items, selected_index):
        """
        Display a menu on the OLED display.

        :param menu_items: A list of tuples where each tuple contains (value, display_text).
        :param selected_index: The index of the currently selected menu item.
        """
        image = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)

        max_lines = self.height // 12  # Assuming 12 pixels per line (10 for font size + 2 for padding)
        start_index = max(0, selected_index - max_lines + 1)
        end_index = min(len(menu_items), start_index + max_lines)

        y = 0
        for i in range(start_index, end_index):
            item = menu_items[i][1]  # Get the display text from the tuple
            if i == selected_index:
                draw.rectangle((0, y, self.width, y + 12), outline=255, fill=255)
                draw.text((2, y), item, font=font, fill=0)
            else:
                draw.text((2, y), item, font=font, fill=255)
            y += 12

        self._display_image_from_image(image)

    def _display_image_from_image(self, image):
        """
        Display an image object on the OLED display.

        :param image: The PIL Image object to display.
        """
        pixel_data = list(image.getdata())
        pages = [0x00] * (self.width * self.pages)

        for i in range(self.height):
            for j in range(self.width):
                if pixel_data[i * self.width + j]:
                    pages[j + (i // 8) * self.width] |= (1 << (i % 8))

        self.write_command(0x22)
        self.write_command(0x00)
        self.write_command(0x07)
        self.write_command(0x21)
        self.write_command(0x00)
        self.write_command(0x7F)

        for page in range(self.pages):
            self.write_command(0xB0 + page)
            self.write_command(0x00)
            self.write_command(0x10)
            self.write_data(pages[page * self.width:(page + 1) * self.width])

    def menu_navigation(self, menu_items, get_encoder_state):
        """
        Navigate through a menu and return the selected value.

        :param menu_items: A list of tuples where each tuple contains (value, display_text).
        :param get_encoder_state: A callback function to get the state of the rotary encoder.
        :return: The selected value from the tuple.
        """
        selected_index = 0
        self.display_menu(menu_items, selected_index)

        while True:
            # get_encoder_state should return a tuple: (rotary_change, button_pressed)
            rotary_change, button_pressed = get_encoder_state()

            if rotary_change > 0:
                selected_index = (selected_index - 1) % len(menu_items)
                self.display_menu(menu_items, selected_index)
                time.sleep(0.2)  # Debounce delay
            elif rotary_change < 0:
                selected_index = (selected_index + 1) % len(menu_items)
                self.display_menu(menu_items, selected_index)
                time.sleep(0.2)  # Debounce delay
            elif button_pressed:
                return menu_items[selected_index][0]  # Return the value from the tuple
            
            time.sleep(0.01)  # Small delay to prevent CPU overuse

    def close(self):
        """
        Close the I2C bus.
        """
        self.clear_display()
        self.bus.close()

    def __enter__(self):
        """
        Enter the context manager.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        self.close()
