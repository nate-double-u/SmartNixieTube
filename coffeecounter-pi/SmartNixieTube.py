__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

from math import log10


class SmartNixieTube:
    """Data structure for the nixie tube display. Represents 1 tube.
    for more info about these nixie tube display drivers, visit http://switchmodedesign.com/products/smart-nixie-tube"""

    def __init__(self, digit='-', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0, red=0, green=0,
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


class SmartNixieTubeDisplay:
    """
    Nixie tube display, this class controls 1 or more tubes connected in series.
    for more info about these nixie tube display drivers, visit http://switchmodedesign.com/products/smart-nixie-tube

    serial data format:
    $[DIGIT],[LEFT DECIMAL POINT],[RIGHT DECIMAL POINT],[BRIGHTNESS],[RED],[GREEN],[BLUE]!
    """

    def __init__(self, numberOfTubesInDisplay):
        self.numberOfTubesInDisplay = numberOfTubesInDisplay
        self.tubes = []

        for i in range(self.numberOfTubesInDisplay):
            self.tubes.append(SmartNixieTube())

    @property
    def numberOfTubesInDisplay(self):
        return self.__numberOfTubesInDisplay

    @numberOfTubesInDisplay.setter
    def numberOfTubesInDisplay(self, value):
        if value < 1:
            raise ValueError('numberOfTubesInDisplay must be greater than 0')
        else:
            self.__numberOfTubesInDisplay = value

    def generateCommandString(self):
        commandString = ''

        for tube in self.tubes:
            commandString = tube.generateCommandString() + commandString

        commandString = commandString + '!'  # add the latch command at the end

        return commandString

    def setDisplayNumber(self, number):
        if number < 0:
            raise ValueError('Display number must be positive')
        elif int(log10(number)) + 1 > self.numberOfTubesInDisplay:
            raise ValueError('Not enough tubes to display all digits')
        else:
            displayNumber = str(number).zfill(self.numberOfTubesInDisplay)
            i = 0
            for tube in self.tubes:
                tube.digit = displayNumber[i]
                i += 1
