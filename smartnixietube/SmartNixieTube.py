__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

from math import log10
import time

import serial


class SmartNixieTubeDisplay:
    """
    Nixie tube display, this class controls 1 or more tubes connected in series.
    for more info about these nixie tube display drivers, visit http://switchmodedesign.com/products/smart-nixie-tube

    serial data format:
    $[DIGIT],[LEFT DECIMAL POINT],[RIGHT DECIMAL POINT],[BRIGHTNESS],[RED],[GREEN],[BLUE]!
    """

    class SmartNixieTube:
        """Data structure for the nixie tube display. Represents 1 tube.
        For more info about these nixie tube display drivers
        visit http://switchmodedesign.com/products/smart-nixie-tube"""

        def __init__(self, digit='-', *, leftdecimalpoint=False, rightdecimalpoint=False, brightness=0, red=0, green=0,
                     blue=0):

            # This is the digit you would like to display on the Nixie Tube.
            self.digit = digit

            # This is the control character for the left decimal point of the Nixie Tube.
            self.leftDecimalPoint = leftdecimalpoint

            # This is the control character for the right decimal point of the Nixie Tube.
            self.rightDecimalPoint = rightdecimalpoint

            # Brightness controls the PWM (brightness) value for the Nixie Tube.
            self.brightness = brightness

            # Red controls the red PWM value for the RGB LED.
            self.red = red

            # Green controls the green PWM value for the RGB LED.
            self.green = green

            # Blue controls the blue PWM value for the RGB LED.
            self.blue = blue

        @property
        def digit(self):
            """This is the digit you would like to display on the Nixie Tube."""
            return self.__digit

        @digit.setter
        def digit(self, value):
            # digit can be 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, or - to turn the Nixie Tube off.
            if value not in '-0123456789':
                self.__digit = '-'
            else:
                self.__digit = value  # This is the digit you would like to display on the Nixie Tube.

        @property
        def leftDecimalPoint(self):
            """This is the control character for the left decimal point of the Nixie Tube."""
            return self.__leftDecimalPoint

        @leftDecimalPoint.setter
        def leftDecimalPoint(self, value):
            if type(value) is not bool:
                raise TypeError('Left decimal point must be of type bool')
            else:
                self.__leftDecimalPoint = value

        @property
        def rightDecimalPoint(self):
            """This is the control character for the left decimal point of the Nixie Tube."""
            return self.__rightDecimalPoint

        @rightDecimalPoint.setter
        def rightDecimalPoint(self, value):
            if type(value) is not bool:
                raise TypeError('Right decimal point must be of type bool')
            else:
                self.__rightDecimalPoint = value

        @property
        def brightness(self):
            """Brightness controls the PWM (brightness) value for the Nixie Tube."""
            return self.__brightness

        @brightness.setter
        def brightness(self, value):
            if value < 0 or value > 255:
                raise ValueError('Brightness must be between 0-255')
            else:
                self.__brightness = value

        @property
        def red(self):
            """Red controls the PWM (brightness) value for the Nixie Tube."""
            return self.__red

        @red.setter
        def red(self, value):
            if value < 0 or value > 255:
                raise ValueError('Red must be between 0-255')
            else:
                self.__red = value

        @property
        def blue(self):
            """Blue controls the PWM (brightness) value for the Nixie Tube."""
            return self.__blue

        @blue.setter
        def blue(self, value):
            if value < 0 or value > 255:
                raise ValueError('Blue must be between 0-255')
            else:
                self.__blue = value

        @property
        def green(self):
            """Green controls the PWM (brightness) value for the Nixie Tube."""
            return self.__green

        @green.setter
        def green(self, value):
            if value < 0 or value > 255:
                raise ValueError('Green must be between 0-255')
            else:
                self.__green = value

        def turnOff(self):
            self.digit = '-'
            self.leftdecimalpoint = False
            self.rightdecimalpoint = False
            self.brightness = 0
            self.red = 0
            self.green = 0
            self.blue = 0

        def convertDigitToStringWithLeadingZeros(self, number):
            return '%03d' % number

        def convertFromBooltoYN(self, boolean):
            if boolean:
                return 'Y'
            else:
                return 'N'

        def generateCommandString(self):
            return (
                '$' +
                self.digit + ',' +
                self.convertFromBooltoYN(self.leftDecimalPoint) + ',' +
                self.convertFromBooltoYN(self.rightDecimalPoint) + ',' +
                self.convertDigitToStringWithLeadingZeros(self.brightness) + ',' +
                self.convertDigitToStringWithLeadingZeros(self.red) + ',' +
                self.convertDigitToStringWithLeadingZeros(self.green) + ',' +
                self.convertDigitToStringWithLeadingZeros(self.blue)
            )
            # end of class SmartNixieTubeProject:

    def __init__(self, numberOfTubesInDisplay, serialPortName='', *, brightness=0, red=0, green=0, blue=0):
        self.numberOfTubesInDisplay = numberOfTubesInDisplay
        self.tubes = []

        # setup the individual tubes in the display
        for i in range(self.numberOfTubesInDisplay):
            self.tubes.append(SmartNixieTubeDisplay.SmartNixieTube())

        # Set the global display values
        # Brightness controls the PWM (brightness) value for the whole Nixie Tube Display.
        self.brightness = brightness

        # Red controls the red PWM value for the RGB LEDs on the whole display.
        self.red = red

        # Green controls the green PWM value for the RGB LEDs on the whole display.
        self.green = green

        # Blue controls the blue PWM value for the RGB LEDs on the whole display.
        self.blue = blue

        # TODO: setup a more automated serial port connection
        # setup serial port stuffs
        self.serialPortName = serialPortName
        if self.serialPortName != '':
            try:
                self.port = serial.Serial(
                    port=self.serialPortName,
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE
                )
                # for i in range(1):  # give the arduino time to reboot b/c opening the serial reboots it...
                #     time.sleep(1)
                # print('.')
            except:
                raise AssertionError('Error opening serial port %s' % self.serialPortName)
        else:
            raise AssertionError('No serial port specified')

    def __del__(self):
        try:
            # turn off the display
            self.reset()
            self.sendCommand()

            # clean up the port.
            self.port.close()
        except:  # TODO: revise this exception. Too broad.
            pass

    @property
    def serialPortName(self):
        return self.__serialPortName

    @serialPortName.setter
    def serialPortName(self, value):
        if type(value) is not str:
            raise TypeError('serialPort must be of type str')
        else:
            self.__serialPortName = value

    @property
    def numberOfTubesInDisplay(self):
        return self.__numberOfTubesInDisplay

    @numberOfTubesInDisplay.setter
    def numberOfTubesInDisplay(self, value):
        if value < 1:
            raise ValueError('numberOfTubesInDisplay must be greater than 0')
        else:
            self.__numberOfTubesInDisplay = value

    @property
    def brightness(self):
        """Brightness controls the PWM (brightness) value for the Nixie Tube."""
        return self.__brightness

    @brightness.setter
    def brightness(self, value):
        if value < 0 or value > 255:
            raise ValueError('Brightness must be between 0-255')
        else:
            self.__brightness = value
            for i in range(self.numberOfTubesInDisplay):
                self.tubes[i].brightness = self.brightness

    @property
    def red(self):
        """Red controls the PWM (brightness) value for the Nixie Tube."""
        return self.__red

    @red.setter
    def red(self, value):
        if value < 0 or value > 255:
            raise ValueError('Red must be between 0-255')
        else:
            self.__red = value
            for i in range(self.numberOfTubesInDisplay):
                self.tubes[i].red = self.red

    @property
    def blue(self):
        """Blue controls the PWM (brightness) value for the Nixie Tube."""
        return self.__blue

    @blue.setter
    def blue(self, value):
        if value < 0 or value > 255:
            raise ValueError('Blue must be between 0-255')
        else:
            self.__blue = value
            for i in range(self.numberOfTubesInDisplay):
                self.tubes[i].blue = self.blue

    @property
    def green(self):
        """Green controls the PWM (brightness) value for the Nixie Tube."""
        return self.__green

    @green.setter
    def green(self, value):
        if value < 0 or value > 255:
            raise ValueError('Green must be between 0-255')
        else:
            self.__green = value
            for i in range(self.numberOfTubesInDisplay):
                self.tubes[i].green = self.green

    def reset(self):
        for tube in self.tubes:
            tube.digit = '-'
            tube.brightness = 0
            tube.red = 0
            tube.green = 0
            tube.blue = 0

    def generateCommandString(self):
        """The first set of data ($1,N,N,128,000,000,255) is going to be passed all the way to the rightmost Smart Nixie
         Tube. The last set of data ($4,N,N,128,000,000,255) is going to be in the leftmost Smart Nixie Tube. Lastly, we
         send the ! in order to tell all of the Smart Nixie Tubes that the data is ready to be latched into their
         display buffer."""

        commandString = ''

        # The serial data is passed from left to right.
        for tube in self.tubes:
            commandString = tube.generateCommandString() + commandString

        # add the latch command at the end to tell the display when the command is done.
        commandString = commandString + '!'

        return commandString

    def setDisplayNumber(self, number):
        # TODO: allow for floats (start using decimal points)
        if number < 0:
            raise ValueError('Display number must be positive')
        elif number == 0:
            displayNumber = str(number).zfill(self.numberOfTubesInDisplay)  # pad the display number with zeroes
            i = 0
            for tube in self.tubes:
                tube.digit = displayNumber[i]
                i += 1
        elif int(log10(number)) + 1 > self.numberOfTubesInDisplay:
            raise ValueError('Not enough tubes to display all digits')
        else:
            displayNumber = str(number).zfill(self.numberOfTubesInDisplay)  # pad the display number with zeroes
            i = 0
            for tube in self.tubes:
                tube.digit = displayNumber[i]
                i += 1

    def sendCommand(self):
        if self.port.isOpen():
            try:
                # do the flushings.
                self.port.flushOutput()
                self.port.flushInput()
                self.port.flush()

                # send the command.
                self.port.write(self.generateCommandString().encode())
                time.sleep(0.1)  # give the display some time to receive the data
            except Exception as e:
                raise ConnectionError(str(e))
