import time, sys, platform, datetime
if platform.system() is not 'Windows':
    import Adafruit_CharLCD as LCD

# https://github.com/adafruit/Adafruit_Python_CharLCD
# Adafruit_GPIO:
# https://github.com/adafruit/Adafruit_Python_GPIO
from scrape import get_departues


def decide_debug():
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'debug':
            return True
    return False


def get_text_w16(rows):
    text=''
    lines = get_departues(rows)
    for i, line in enumerate(lines):
        if i < len(lines)-1:
            text += '{:<4}{:>12}\n'.format(line['bus'], line['arrival'])
        else:
            text += '{:<4}{:>12}'.format(line['bus'], line['arrival'])
    return text


def setup_lcd():
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
    return lcd


def log_error(exception):
    with open('error_log.txt', 'a+') as f:
        f.write('{} : {}\n'.format(datetime.datetime.now(), exception))


def write_to_log(message):
    with open('error_log.txt', 'a+') as f:
        f.write('{} : {}\n'.format(datetime.datetime.now(), message))


def restart():
    write_to_log('Restaring...')
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def main():
    write_to_log('Started pi')
    debug = decide_debug()
    if not debug:
        lcd = setup_lcd()
        while True:
            try:
                text = get_text_w16(2)
                lcd.clear()
                lcd.message(text)
            except Exception as e:
                log_error(e)
                restart()
            time.sleep(20)
    else:
        while True:
            try:
                text = get_text_w16(2)
                print(text)
            except Exception as e:
                log_error(e)
            time.sleep(10)

if __name__ == "__main__":
    main()
