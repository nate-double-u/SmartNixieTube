__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

import random

from SmartNixieTube import SmartNixieTubeDisplay

numberOfTubesInDisplay = 3
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, '/dev/tty.usbserial-A9QHHRFJ')  # '/dev/tty.usbserial-A9UD9RRV')

display.brightness = 255

for i in range(255):
    display.red = random.randint(0,255)
    display.green = random.randint(0,255)
    display.blue = random.randint(0,255)

    display.setDisplayNumber(i)  # random.randint(0,999))

    # print(i, display.generateCommandString().encode())

    display.sendCommand()
