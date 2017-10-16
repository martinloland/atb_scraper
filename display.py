import time
import Adafruit_CharLCD as LCD
# https://github.com/adafruit/Adafruit_Python_CharLCD
# Adafruit_GPIO:
# https://github.com/adafruit/Adafruit_Python_GPIO
from scrape import get_departues


def get_text_w16(rows):
    text=''
    lines = get_departues(rows)
    for i, line in enumerate(lines):
        if i < len(lines)-1:
            text += '{:<4}{:>12}\n'.format(line['bus'], line['arrival'])
        else:
            text += '{:<4}{:>12}'.format(line['bus'], line['arrival'])
    return text

# while True:
#     print(get_text_w16(rows=2))
#     time.sleep(30)


# Raspberry Pi pin configuration:
lcd_rs        = 26
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 15

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.message('Hello\nworld!')