#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'graphics')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'driver')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
print(picdir)
from driver import waveshare
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

def makeImage(batPerc, con, gen):
    logging.info("Drawing image")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    draw.text((55, 0), u'iglü smart home', font = font24, fill = 0)
    bat = Image.open(os.path.join(picdir, 'battery-half.bmp'))
    solar = Image.open(os.path.join(picdir, 'solar.bmp'))
    bolt = Image.open(os.path.join(picdir, 'bolt.bmp'))
    image.paste(solar, (10,40))
    image.paste(bolt, (120,40))
    image.paste(bat, (200,40))
    draw.text((205, 85), str(batPerc) +'%', font = font15, fill = 0)
    draw.text((110, 85), str(con) +'kW', font = font15, fill = 0)
    draw.text((15, 85), str(gen) + 'kW', font = font15, fill = 0)
    draw.text((120, 105), 'local.nacdlow.com', font = font15, fill = 0)

    draw.text((205, 20), 'Bat', font = font15, fill = 0)
    draw.text((120, 20), 'Con', font = font15, fill = 0)
    draw.text((25, 20), 'Gen', font = font15, fill = 0)
    return image

try:
    logging.info("iglu e-ink service")
    
    epd = waveshare.EPD()
    logging.info("Clearing the display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.debug("Size: " + str(epd.width) + ", " + str(epd.height))
    
    # Drawing on the image
    image = makeImage(10, 123, 40)
    epd.display(epd.getbuffer(image))

    # Set mode to partial update
    epd.init(epd.PART_UPDATE)
    batPerc = 5

    while True:
        image = makeImage(batPerc, 11, 40)
        epd.displayPartial(epd.getbuffer(image))
        print("waiting")
        batPerc += 10
        time.sleep(3)

    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("Exiting...")
    waveshare.epdconfig.module_exit()
    exit()

