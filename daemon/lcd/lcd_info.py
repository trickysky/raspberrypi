#!/usr/bin/python
# -*- coding: UTF-8 -*-
# trickysky

import time, datetime
import Adafruit_Nokia_LCD as LCD
from PIL import Image, ImageDraw, ImageFont
import utility as util

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
font_default = ImageFont.load_default()
font_time = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf', 12)
font_ip = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 10)
font_noip = font_default
font_content = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 10)

while True:
    # Draw a white filled box to clear the image.
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

    # Write some text.
    draw.text((16, 1), str(time.strftime('%H:%M:%S')), font=font_time)
    draw.line((0, 15, LCD.LCDWIDTH, 15))

    content1_loc = (0, 20)
    content2_loc = (0, 32)
    second = datetime.datetime.now().second

    if second % 20 in range(0, 8, 1):
        if util.network('eth0').is_connect():
            draw.text(content1_loc, util.network('eth0').get_ip(), font=font_ip)
        else:
            draw.text(content1_loc, '-- no lan --', font=font_noip)
        if util.network('wlan0').is_connect():
            if second % 20 in range(0, 4, 1):
                draw.text(content2_loc, util.network('wlan0').get_ip(), font=font_ip)
            else:
                ssid = util.network('wlan0').get_ssid()
                draw.text(content2_loc, ssid, font=font_default)
        else:
            draw.text(content2_loc, '-- no wifi --', font=font_noip)
    elif second % 20 in range(8, 14, 1):
        draw.text(content1_loc, "CPU : %s%%" % util.get_cpu_percent(), font=font_content)
        draw.text(content2_loc, "RAM : %s" % util.get_ram_info()[2], font=font_content)
    else:
        draw.text(content1_loc, "DISK Free: %s" % util.get_disk_space()[2], font=font_content)
        draw.text(content2_loc, "CPU Temp: %s 'C" % util.get_cpu_temperature(), font=font_content)

    # Display image.
    disp.image(image)
    disp.display()

    time.sleep(0.25)
