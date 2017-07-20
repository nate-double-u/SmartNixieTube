import random

__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

try:
    from smartnixietube.SmartNixieTubeDisplay import SmartNixieTubeDisplay
except ImportError as e:
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from smartnixietube.SmartNixieTubeDisplay import SmartNixieTubeDisplay

# set number of tubes in the display
numberOfTubesInDisplay = 3

# instantiate the display -- serial ports tested on Linux and Mac OS X.
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, '/dev/tty.usbserial-A9QHHRFJ')  # '/dev/tty.usbserial-A9UD9RRV')

# all the properties can be set like this:
display.brightness = 255

for i in range(255):
    display.red = random.randint(0, 255)
    display.green = random.randint(0, 255)
    display.blue = random.randint(0, 255)

    # set the display number
    display.set_display_number(i)  # random.randint(0,999))

    # send the command set to the display
    display.send_command()
