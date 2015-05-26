__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

from SmartNixieTube import SmartNixieTubeDisplay
import time
import random

numberOfTubesInDisplay = 3
display = SmartNixieTubeDisplay(numberOfTubesInDisplay, '/dev/tty.usbserial-A9QHHRFJ')  # '/dev/tty.usbserial-A9UD9RRV')

# # set colour of leds
# display.red = 255
# display.green = 165
# display.blue = 0
#
# # remember to set the brightness of the digits
# display.brightness = 128
#
# # set the number to display
# display.setDisplayNumber(4)
#
# # show us the command string getting sent
# print(display.generateCommandString().encode())
#
# # send it!
# display.sendCommand()
#
# # set colour of leds
# # set colour of leds
# display.red = 0
# display.green = 89
# display.blue = 255
#
# # set the number to display
# display.setDisplayNumber(5)
#
# # show us the command string getting sent
# print(display.generateCommandString().encode())
#
# # send it!
# display.sendCommand()

display.brightness = 255

for i in range(200):
    display.red = random.randint(0,255)
    display.green = random.randint(0,255)
    display.blue = random.randint(0,255)

    display.setDisplayNumber(random.randint(0,999))

    # print(i, display.generateCommandString().encode())

    display.sendCommand()
