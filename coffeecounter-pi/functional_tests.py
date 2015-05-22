__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

import random
import time

from SmartNixieTube import SmartNixieTubeDisplay


# functional tests
numberOfTubesInDisplay = 3
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, serialPort='/dev/cu.usbserial-A9QHHRFJ')
display.brightness = 128
display.openSerialPort()

for i in range(30):
    numberToDisplay = random.randint(0, 999)
    display.setDisplayNumber(numberToDisplay)
    display.sendCommand()
    time.sleep(1)  # wait a second...
