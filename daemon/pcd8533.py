#!/usr/bin/python
# -*- coding: UTF-8 -*-
# trickysky

import time
import wiringpi
import spidev
from PIL import Image, ImageDraw, ImageFont

# White backlight
# CONTRAST = 0xa4

# Blue backlight
CONTRAST = 0xa4

ROWS = 6
COLUMNS = 14
PIXELS_PER_ROW = 6
ON = 1
OFF = 0

# gpio's :
DC = 3  # gpio pin 15 = wiringpi no. 3 (BCM 22)
RST = 0  # gpio pin 11 = wiringpi no. 0 (BCM 17)
LED = 1  # gpio pin 12 = wiringpi no. 1 (BCM 18)

# SPI connection
SCE = 10  # gpio pin 24 = wiringpi no. 10 (CE0 BCM 8)
SCLK = 14  # gpio pin 23 = wiringpi no. 14 (SCLK BCM 11)
DIN = 12  # gpio pin 19 = wiringpi no. 12 (MOSI BCM 10)

CLSBUF = [0] * (ROWS * COLUMNS * PIXELS_PER_ROW)

FONT = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x00, 0x00, 0x5f, 0x00, 0x00],
    '"': [0x00, 0x07, 0x00, 0x07, 0x00],
    '#': [0x14, 0x7f, 0x14, 0x7f, 0x14],
    '$': [0x24, 0x2a, 0x7f, 0x2a, 0x12],
    '%': [0x23, 0x13, 0x08, 0x64, 0x62],
    '&': [0x36, 0x49, 0x55, 0x22, 0x50],
    "'": [0x00, 0x05, 0x03, 0x00, 0x00],
    '(': [0x00, 0x1c, 0x22, 0x41, 0x00],
    ')': [0x00, 0x41, 0x22, 0x1c, 0x00],
    '*': [0x14, 0x08, 0x3e, 0x08, 0x14],
    '+': [0x08, 0x08, 0x3e, 0x08, 0x08],
    ',': [0x00, 0x50, 0x30, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '0': [0x3e, 0x51, 0x49, 0x45, 0x3e],
    '1': [0x00, 0x42, 0x7f, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4b, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7f, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3c, 0x4a, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1e],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    ';': [0x00, 0x56, 0x36, 0x00, 0x00],
    '<': [0x08, 0x14, 0x22, 0x41, 0x00],
    '=': [0x14, 0x14, 0x14, 0x14, 0x14],
    '>': [0x00, 0x41, 0x22, 0x14, 0x08],
    '?': [0x02, 0x01, 0x51, 0x09, 0x06],
    '@': [0x32, 0x49, 0x79, 0x41, 0x3e],
    'A': [0x7e, 0x11, 0x11, 0x11, 0x7e],
    'B': [0x7f, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3e, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7f, 0x41, 0x41, 0x22, 0x1c],
    'E': [0x7f, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7f, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3e, 0x41, 0x49, 0x49, 0x7a],
    'H': [0x7f, 0x08, 0x08, 0x08, 0x7f],
    'I': [0x00, 0x41, 0x7f, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3f, 0x01],
    'K': [0x7f, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7f, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7f, 0x02, 0x0c, 0x02, 0x7f],
    'N': [0x7f, 0x04, 0x08, 0x10, 0x7f],
    'O': [0x3e, 0x41, 0x41, 0x41, 0x3e],
    'P': [0x7f, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3e, 0x41, 0x51, 0x21, 0x5e],
    'R': [0x7f, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7f, 0x01, 0x01],
    'U': [0x3f, 0x40, 0x40, 0x40, 0x3f],
    'V': [0x1f, 0x20, 0x40, 0x20, 0x1f],
    'W': [0x3f, 0x40, 0x38, 0x40, 0x3f],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    '[': [0x00, 0x7f, 0x41, 0x41, 0x00],
    '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
    ']': [0x00, 0x41, 0x41, 0x7f, 0x00],
    '^': [0x04, 0x02, 0x01, 0x02, 0x04],
    '_': [0x40, 0x40, 0x40, 0x40, 0x40],
    '`': [0x00, 0x01, 0x02, 0x04, 0x00],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'b': [0x7f, 0x48, 0x44, 0x44, 0x38],
    'c': [0x38, 0x44, 0x44, 0x44, 0x20],
    'd': [0x38, 0x44, 0x44, 0x48, 0x7f],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    'f': [0x08, 0x7e, 0x09, 0x01, 0x02],
    'g': [0x0c, 0x52, 0x52, 0x52, 0x3e],
    'h': [0x7f, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7d, 0x40, 0x00],
    'j': [0x20, 0x40, 0x44, 0x3d, 0x00],
    'k': [0x7f, 0x10, 0x28, 0x44, 0x00],
    'l': [0x00, 0x41, 0x7f, 0x40, 0x00],
    'm': [0x7c, 0x04, 0x18, 0x04, 0x78],
    'n': [0x7c, 0x08, 0x04, 0x04, 0x78],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'p': [0x7c, 0x14, 0x14, 0x14, 0x08],
    'q': [0x08, 0x14, 0x14, 0x18, 0x7c],
    'r': [0x7c, 0x08, 0x04, 0x04, 0x08],
    's': [0x48, 0x54, 0x54, 0x54, 0x20],
    't': [0x04, 0x3f, 0x44, 0x40, 0x20],
    'u': [0x3c, 0x40, 0x40, 0x20, 0x7c],
    'v': [0x1c, 0x20, 0x40, 0x20, 0x1c],
    'w': [0x3c, 0x40, 0x30, 0x40, 0x3c],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'y': [0x0c, 0x50, 0x50, 0x50, 0x3c],
    'z': [0x44, 0x64, 0x54, 0x4c, 0x44],
    '{': [0x00, 0x08, 0x36, 0x41, 0x00],
    '|': [0x00, 0x00, 0x7f, 0x00, 0x00],
    '}': [0x00, 0x41, 0x36, 0x08, 0x00],
    '~': [0x10, 0x08, 0x08, 0x10, 0x08],
    '\x7f': [0x00, 0x7e, 0x42, 0x42, 0x7e],
}

ORIGINAL_CUSTOM = FONT['\x7f']


def bit_reverse(value, width=8):
    result = 0
    for _ in xrange(width):
        result = (result << 1) | (value & 1)
        value >>= 1

    return result


BITREVERSE = map(bit_reverse, xrange(256))


class NokiaSPI:
    def __init__(self, dev=(0, 0), speed=5000000, brightness=256, contrast=CONTRAST):
        self.spi = spidev.SpiDev()
        self.speed = speed
        self.dev = dev
        self.spi.open(self.dev[0], self.dev[1])
        self.spi.max_speed_hz = self.speed

        # Set pin directions.
        self.dc = DC
        self.rst = RST
        wiringpi.wiringPiSetup()
        for pin in [self.dc, self.rst]:
            wiringpi.pinMode(pin, 1)

        self.contrast = contrast
        self.brightness = brightness

        # Toggle RST low to reset.
        wiringpi.digitalWrite(self.rst, OFF)
        time.sleep(0.100)
        wiringpi.digitalWrite(self.rst, ON)
        # Extended mode, bias, vop, basic mode, non-inverted display.
        wiringpi.digitalWrite(self.dc, OFF)
        self.spi.writebytes([0x21, 0x14, self.contrast, 0x20, 0x0c])
        # cls()

        self.ledpin = LED
        if self.ledpin == 1:
            wiringpi.pinMode(self.ledpin, 2)
            wiringpi.pwmWrite(self.ledpin, self.brightness)
        else:
            wiringpi.pinMode(self.ledpin, 1)
            wiringpi.digitalWrite(self.ledpin, ON)

    def lcd_cmd(self, value):
        wiringpi.digitalWrite(self.dc, OFF)
        self.spi.writebytes([value])

    def lcd_data(self, value):
        wiringpi.digitalWrite(self.dc, ON)
        self.spi.writebytes([value])

    def gotoxy(self, x, y):
        wiringpi.digitalWrite(self.dc, OFF)
        self.spi.writebytes([x + 128, y + 64])

    def cls(self):
        self.gotoxy(0, 0)
        wiringpi.digitalWrite(self.dc, ON)
        self.spi.writebytes(CLSBUF)

    def led(self, led_value):
        if self.ledpin == 1:
            wiringpi.pwmWrite(self.ledpin, led_value)
        else:
            if led_value == 0:
                wiringpi.digitalWrite(self.ledpin, OFF)
            else:
                wiringpi.digitalWrite(self.ledpin, ON)

    def load_bitmap(self, filename, reverse=False):
        mask = 0xff if reverse else 0x00
        self.gotoxy(0, 0)
        with open(filename, 'rb') as bitmap_file:
            for x in xrange(6):
                for y in xrange(84):
                    bitmap_file.seek(0x3e + y * 8 + x)
                    self.lcd_data(BITREVERSE[ord(bitmap_file.read(1))] ^ mask)

    def show_custom(self, font=FONT):
        self.display_char('\x7f', font)

    def define_custom(self, values):
        FONT['\x7f'] = values

    def restore_custom(self):
        self.define_custom(ORIGINAL_CUSTOM)

    def alt_custom(self):
        self.define_custom([0x00, 0x50, 0x3C, 0x52, 0x44])

    def pi_custom(self):
        self.define_custom([0x19, 0x25, 0x5A, 0x25, 0x19])

    def display_char(self, char, font=FONT):
        try:
            wiringpi.digitalWrite(self.dc, ON)
            self.spi.writebytes(font[char] + [0])

        except KeyError:
            pass  # Ignore undefined characters.

    def text(self, string, font=FONT):
        for char in string:
            self.display_char(char, font)

    def gotorc(self, r, c):
        self.gotoxy(c * 6, r)

    def centre_word(self, r, word):
        self.gotorc(r, max(0, (COLUMNS - len(word)) // 2))
        self.text(word)

    def show_image(self, im):
        # Rotate and mirror the image
        rim = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)

        # Change display to vertical write mode for graphics
        wiringpi.digitalWrite(DC, OFF)
        self.spi.writebytes([0x22])

        # Start at upper left corner
        self.gotoxy(0, 0)
        # Put on display with reversed bit order
        wiringpi.digitalWrite(DC, ON)
        self.spi.writebytes([BITREVERSE[ord(x)] for x in list(rim.tostring())])

        # Switch back to horizontal write mode for text
        wiringpi.digitalWrite(DC, OFF)
        self.spi.writebytes([0x20])


if __name__ == '__main__':
    start, end = 32, 116
    print 'LCD Display Test: ASCII %d to %d' % (start, end)
    # do not include init() in the timing tests
    ## init()
    noki = NokiaSPI()
    start_time = time.time()
    noki.cls()
    noki.led(768)
    for i in xrange(start, end):
        noki.display_char(chr(i))

    finish_time = time.time()
    print 'Cls, LED on, %d chars, total time = %.3f' % (
        end - start, finish_time - start_time
    )

    time.sleep(1)

    # Test a custom character for 0x7f (supposed to be a bell)
    # . . . - - - - -
    # . . . - - X - -
    # . . . - X X X -
    # . . . - X - X -
    # . . . X - - - X
    # . . . X X X X X
    # . . . - - X X -
    # . . . - - - - -
    noki.define_custom([0x30, 0x2c, 0x66, 0x6c, 0x30])

    noki.cls()
    noki.text("\x7f \x7f \x7f \x7f \x7f \x7f \x7f ")
    noki.text("    Hello     ")
    noki.text(" Raspberry Pi")

    # Backlight PWM testing -- off -> 25% -> off
    # for i in range(0,255):
    #  noki.led(i)
    #  time.sleep(0.025)
    # for i in range(255,0,-1):
    #  noki.led(i)
    #  time.sleep(0.025)

    time.sleep(1)

    ## Generate an image with PIL and put on the display
    ## First time through is slow as the fonts are not cached
    ##
    start_time = time.time()
    # load an available True Type font
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 14)

    # New b-w image
    im = Image.new('1', (84, 48))
    # New drawable on image
    draw = ImageDraw.Draw(im)
    # Full screen and half-screen ellipses
    draw.ellipse((0, 0, im.size[0] - 1, im.size[1] - 1), outline=1)
    draw.ellipse((im.size[0] / 4, im.size[1] / 4, im.size[0] / 4 * 3 - 1, im.size[1] / 4 * 3 - 1), outline=1)
    # Some simple text for a test (first with TT font, second with default
    draw.text((10, 10), "hello", font=font, fill=1)
    draw.text((10, 24), "world", fill=1)
    # Check what happens when text exceeds width (clipped)
    draw.text((0, 0), "ABCabcDEFdefGHIghi", fill=1)
    # Copy it to the display
    noki.show_image(im)
    # clean up
    del draw
    del im

    finish_time = time.time()
    print 'PIL Drawing, total time = %.3f' % (finish_time - start_time)