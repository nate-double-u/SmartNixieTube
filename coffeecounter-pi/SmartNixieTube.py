__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'


class SmartNixieTube():
    """Data structure for the nixie tube display. Represents 1 tube.
    for more info about these nixie tube display drivers, visit http://switchmodedesign.com/products/smart-nixie-tube"""

    def __init__(self, digit='-', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0, red=0, green=0,
                 blue=0):
        # digit can be 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, or - to turn the Nixie Tube off.
        if digit not in '-0123456789':
            raise AssertionError('Values for digit must be one of "0123456789-"')
        else:
            self.digit = digit  # This is the digit you would like to display on the Nixie Tube.

        if type(leftdecimalpoint) is not bool:
            raise AssertionError('Left decimal point must be of type bool')
        else:
            # This is the control character for the left decimal point of the Nixie Tube.
            self.leftDecimalPoint = leftdecimalpoint

        if type(rightdecimalpoint) is not bool:
            raise AssertionError('Right decimal point must be of type bool')
        else:
            # This is the control character for the right decimal point of the Nixie Tube.
            self.rightDecimalPoint = rightdecimalpoint

        if brightness < 0 or brightness > 255:
            raise AssertionError('Brightness must be between 0-255')
        else:
            self.brightness = brightness  # Brightness controls the PWM (brightness) value for the Nixie Tube.

        if red < 0 or red > 255:
            raise AssertionError('Red must be between 0-255')
        else:
            self.red = red  # Red controls the red PWM value for the RGB LED.
        if green < 0 or green > 255:
            raise AssertionError('Green must be between 0-255')
        else:
            self.green = green  # Green controls the green PWM value for the RGB LED.

        if blue < 0 or blue > 255:
            raise AssertionError('Blue must be between 0-255')
        else:
            self.blue = blue  # Blue controls the blue PWM value for the RGB LED.

    def turnOff(self):
        self.digit='-'
        self.leftdecimalpoint=False
        self.rightdecimalpoint=False
        self.brightness=0
        self.red=0
        self.green=0
        self.blue=0

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


class SmartNixieTubeDisplay():
    """
    Nixie tube display, this class controls 1 or more tubes connected in series.
    for more info about these nixie tube display drivers, visit http://switchmodedesign.com/products/smart-nixie-tube

    serial data format:
    $[DIGIT],[LEFT DECIMAL POINT],[RIGHT DECIMAL POINT],[BRIGHTNESS],[RED],[GREEN],[BLUE]!
    """

    def __init__(self, numberOfTubesInDisplay):
        if numberOfTubesInDisplay < 1:
            raise AssertionError('Must have one or more tubes.')

        self.numberOfTubesInDisplay = numberOfTubesInDisplay
