import unittest

try:
    from smartnixietube.SmartNixieTube import SmartNixieTube
except ImportError as e:
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from smartnixietube.SmartNixieTube import SmartNixieTube

__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'


class TestSmartNixieTube(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_digit_in_range(self):
        tube = SmartNixieTube(digit='0')
        self.assertEqual('0', tube.digit)

    def test_init_digits_out_of_range(self):
        tube = SmartNixieTube(digit='=', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=0,
                                                    red=0, green=0,
                                                    blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_digits_not_a_number(self):
        tube = SmartNixieTube(digit='A', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=0,
                                                    red=0, green=0,
                                                    blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_leftDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError,
                              SmartNixieTube(left_decimal_point=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('Left decimal point must be of type bool', str(e))

    def test_init_rightDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError,
                              SmartNixieTube(right_decimal_point=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('Right decimal point must be of type bool', str(e))

    def test_init_brightness_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTube(brightness=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTube(brightness=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

    def test_init_red_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTube(red=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTube(red=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

    def test_init_blue_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTube(blue=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTube(blue=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

    def test_init_green_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTube(green=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTube(green=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

    def test_init_defaults(self):
        tube = SmartNixieTube()
        self.assertEqual('-', tube.digit)
        self.assertEqual(False, tube.left_decimal_point)
        self.assertEqual(False, tube.right_decimal_point)
        self.assertEqual(0, tube.brightness)
        self.assertEqual(0, tube.blue)
        self.assertEqual(0, tube.green)
        self.assertEqual(0, tube.red)

    def test_convertDigitToStringWithLeadingZeros(self):
        tube = SmartNixieTube()
        self.assertEqual('000', tube.convert_digit_to_string_with_leading_zeros(0))
        self.assertEqual('001', tube.convert_digit_to_string_with_leading_zeros(1))
        self.assertEqual('010', tube.convert_digit_to_string_with_leading_zeros(10))
        self.assertEqual('100', tube.convert_digit_to_string_with_leading_zeros(100))

    def test_convertFromBoolToYN(self):
        tube = SmartNixieTube()
        self.assertEqual(tube.convert_from_bool_to_yn(True), 'Y')
        self.assertEqual(tube.convert_from_bool_to_yn(False), 'N')

    def test_generateCommandString(self):
        tube = SmartNixieTube()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generate_command_string())

        tube2 = SmartNixieTube('9', left_decimal_point=False, right_decimal_point=False,
                                                     brightness=128, red=0, green=255, blue=255)
        self.assertEqual('$9,N,N,128,000,255,255', tube2.generate_command_string())

        tube3 = SmartNixieTube('5', left_decimal_point=False, right_decimal_point=False,
                                                     brightness=28, red=0, green=10, blue=1)
        self.assertEqual('$5,N,N,028,000,010,001', tube3.generate_command_string())

    def test_LeftDecimalCommandString(self):
        tube = SmartNixieTube(left_decimal_point=True)
        self.assertEqual('$-,Y,N,000,000,000,000', tube.generate_command_string())

    def test_RightDecimalCommandString(self):
        tube = SmartNixieTube(right_decimal_point=True)
        self.assertEqual('$-,N,Y,000,000,000,000', tube.generate_command_string())

    def test_turnOff(self):
        # turn on anything, check that it's on
        tube = SmartNixieTube('9', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=128, red=0, green=255, blue=255)
        self.assertEqual('$9,N,N,128,000,255,255', tube.generate_command_string())

        # test that the generate command string sends out zeros and a dash after turn_off()
        tube.turn_off()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generate_command_string())


if __name__ == '__main__':
    # run unit tests
    unittest.main(warnings='ignore')
