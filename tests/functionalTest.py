__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

import random

try:
    from smartnixietube.SmartNixieTube import SmartNixieTubeDisplay
except ImportError as e:
    import sys
    import os
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from smartnixietube.SmartNixieTube import SmartNixieTubeDisplay

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
