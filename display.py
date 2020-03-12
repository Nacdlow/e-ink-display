from PIL import Image
from includes.epd import Epd
from includes.icon import Icon
from includes.text import Text

import spidev as SPI
import os
import time

import urllib.request
import ssl
import json
import socket
from time import sleep, gmtime, strftime

# Ignore SSL certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://localhost:8080/sim/data.json"

while True:
    jsonData = urllib.request.urlopen(url, context=ctx).read()
    parsedData = json.loads(jsonData)

    batteryMax = parsedData["home"]["solar_max_power"]
    currBattery = round(parsedData["home"]["battery_store"], 2)
    usage = round(parsedData["home"]["power_con_rate"], 2)
    generation = round(parsedData["home"]["power_gen_rate"], 2)

    if currBattery < 0:
        currBattery = 0

    batteryPercentage = round((currBattery / batteryMax) * 100)

    # Function to display hostname and IP address
    def get_Host_name_IP():
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print(host_ip)
        except:
            print("Unable to get Hostname and IP")

    get_Host_name_IP()

    print(strftime("%H:%M %d/%m/%Y", gmtime()))
    # print("Battery Capacity: " + str(batteryMax) + " kWh")
    print("Current Store: " + str(currBattery) + " kWh")
    print("Battery Percentage: " + str(batteryPercentage) + "%")
    print("Power Usage: " + str(usage) + " kWh")
    print("Power Generation: " + str(generation) + " kWh")
    print("")
    sleep(3)
    # print(json.dumps(parsedData["minecraft_time"], indent=2, sort_keys=True))

    # print(parsedData)


WHITE = 1
BLACK = 0
DISPLAY_TYPE = 'EPD_2X9'
ICON_SIZE = 100


def main():
    bus, device = 0, 0
    spi = SPI.SpiDev(bus, device)
    display = Epd(spi, DISPLAY_TYPE)

    print('--> Init and clear full screen %s' % display.size)
    display.clearDisplayPart()

    while True:
        for file in os.listdir("./png-icons/%d/" % ICON_SIZE):
            if file.endswith(".png"):
                # display width and height
                height, width = display.size

                # canvas to draw to
                image = Image.new('1', display.size, WHITE)

                # add icon to canvas
                icon = Icon(image, os.path.join(
                    ("./png-icons/%d/" % ICON_SIZE), file))
                print("--> Prepare PNG: %s (size: %d x %d)" %
                      (file, icon.width, icon.height))

                # add text beside the icon
                text = Text(width-128, height, file)
                image.paste(text.image, (0, 128, 128, 296), mask=BLACK)

                # send image to display
                display.showImageFull(display.imageToPixelArray(image))

                time.sleep(2)
                display.clearDisplayPart()


# main
if "__main__" == __name__:
    main()
