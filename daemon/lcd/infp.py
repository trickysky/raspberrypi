#!/usr/bin/python
# -*- coding: UTF-8 -*-
# trickysky

import sys
import time
import Adafruit_Nokia_LCD as LCD
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Raspberry Pi software SPI config:
SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 22

# Software SPI usage (defaults to bit-bang SPI interface):
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=10)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

# Load default font.
print '%s/src/fonts/Consolas.ttf' % Path(sys.path[0]).parent.parent
font = ImageFont.truetype('%s/src/fonts/Consolas.ttf' % Path(sys.path[0]).parent.parent, 30)

# Write some text.
draw.text((0,0), 'tiankun1  ')
draw.text((0,14), '192.168.199.104')

# Display image.
disp.image(image)
disp.display()

quit()
