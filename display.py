# import Adafruit_CharLCD as LCD
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

print(get_text_w16(rows=2))

# # Raspberry Pi pin configuration:
# lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
# lcd_en        = 22
# lcd_d4        = 25
# lcd_d5        = 24
# lcd_d6        = 23
# lcd_d7        = 18
# lcd_backlight = 4
#
# # Define LCD column and row size for 16x2 LCD.
# lcd_columns = 16
# lcd_rows    = 2
#
# # Initialize the LCD using the pins above.
# lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
#                            lcd_columns, lcd_rows, lcd_backlight)
#
# # Print a two line message
# lcd.message('Hello\nworld!')