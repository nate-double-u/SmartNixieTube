import random
import threading

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
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, '/dev/ttyUSB0')  # '/dev/tty.usbserial-A9UD9RRV')

# all the properties can be set like this:
display.brightness = 255


# set random number every second
def set_number():
    global display
    threading.Timer(1.0, set_number).start()
    display.set_display_number(random.randint(0, 999))

set_number()

# do the thing
for i in range(255):
    display.red = random.randint(0, 255)
    display.green = random.randint(0, 255)
    display.blue = random.randint(0, 255)

    # set the display number
    # display.set_display_number(i)  # random.randint(0,999))

    # send the command set to the display
    display.send_command()
