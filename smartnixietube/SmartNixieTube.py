__author__ = 'Nate Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'


class SmartNixieTube:
    """Data structure for the nixie tube display. Represents 1 tube.
    For more info about these nixie tube display drivers
    visit http://switchmodedesign.com/products/smart-nixie-tube"""

    def __init__(self, digit='-', *, left_decimal_point=False, right_decimal_point=False, brightness=0, red=0,
                 green=0, blue=0):

        # This is the digit you would like to display on the Nixie Tube.
        self.digit = digit

        # This is the control character for the left decimal point of the Nixie Tube.
        self.left_decimal_point = left_decimal_point

        # This is the control character for the right decimal point of the Nixie Tube.
        self.right_decimal_point = right_decimal_point

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
    def left_decimal_point(self):
        """This is the control character for the left decimal point of the Nixie Tube."""
        return self.__left_decimal_point

    @left_decimal_point.setter
    def left_decimal_point(self, value):
        if type(value) is not bool:
            raise TypeError('Left decimal point must be of type bool')
        else:
            self.__left_decimal_point = value

    @property
    def right_decimal_point(self):
        """This is the control character for the left decimal point of the Nixie Tube."""
        return self.__right_decimal_point

    @right_decimal_point.setter
    def right_decimal_point(self, value):
        if type(value) is not bool:
            raise TypeError('Right decimal point must be of type bool')
        else:
            self.__right_decimal_point = value

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

    def turn_off(self):
        self.digit = '-'
        self.left_decimal_point = False
        self.right_decimal_point = False
        self.brightness = 0
        self.red = 0
        self.green = 0
        self.blue = 0

    @staticmethod
    def convert_digit_to_string_with_leading_zeros(number):
        return '%03d' % number

    @staticmethod
    def convert_from_bool_to_yn(boolean):
        if boolean:
            return 'Y'
        else:
            return 'N'

    def generate_command_string(self):
        return (
            '$' +
            self.digit + ',' +
            self.convert_from_bool_to_yn(self.left_decimal_point) + ',' +
            self.convert_from_bool_to_yn(self.right_decimal_point) + ',' +
            self.convert_digit_to_string_with_leading_zeros(self.brightness) + ',' +
            self.convert_digit_to_string_with_leading_zeros(self.red) + ',' +
            self.convert_digit_to_string_with_leading_zeros(self.green) + ',' +
            self.convert_digit_to_string_with_leading_zeros(self.blue)
        )
