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

import spidev as SPI
import collections

import urllib.request
import ssl
import json
import socket
from time import sleep, gmtime, strftime

# Ignore SSL certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://serow.alq/sim/data.json"
SimData = collections.namedtuple('sim_data', ['generation', 'usage', 'battery'])

def getData():
    jsonData = urllib.request.urlopen(url, context=ctx).read()
    parsedData = json.loads(jsonData)

    batteryMax = parsedData["home"]["solar_max_power"]
    currBattery = round(parsedData["home"]["battery_store"], 2)
    usage = round(parsedData["home"]["power_con_rate"], 2)
    generation = round(parsedData["home"]["power_gen_rate"], 2)

    if currBattery < 0:
        currBattery = 0

    batteryPercentage = round((currBattery / batteryMax) * 100)

    # print("Battery Capacity: " + str(batteryMax) + " kWh")
    print("Current Store: " + str(currBattery) + " kWh")
    print("Battery Percentage: " + str(batteryPercentage) + "%")
    print("Power Usage: " + str(usage) + " kWh")
    print("Power Generation: " + str(generation) + " kWh")
    return SimData(generation = int(generation), usage = int(usage),
            battery = int(batteryPercentage))


def makeImage(batPerc, con, gen):
    logging.info("Loading data from sim...")
    dat = getData()
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
    draw.text((205, 85), str(dat.battery) +'%', font = font15, fill = 0)
    draw.text((110, 85), str(dat.generation) +'kW', font = font15, fill = 0)
    draw.text((15, 85), str(dat.usage) + 'kW', font = font15, fill = 0)
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
        buf = epd.getbuffer(image)
        epd.displayPartial(buf)
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
