__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

from SmartNixieTube import SmartNixieTubeDisplay
import time
import random

numberOfTubesInDisplay = 3
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, '/dev/tty.usbserial-A9QHHRFJ')  # '/dev/tty.usbserial-A9UD9RRV')

display.brightness = 255

for i in range(255):
    display.red = i  # random.randint(0,255)
    display.green = i  # random.randint(0,255)
    display.blue = i  # random.randint(0,255)

    display.setDisplayNumber(i)  # random.randint(0,999))

    # print(i, display.generateCommandString().encode())

    display.sendCommand()
