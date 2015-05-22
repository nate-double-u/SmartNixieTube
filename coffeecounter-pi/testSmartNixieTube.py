__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

import unittest

from SmartNixieTube import SmartNixieTubeDisplay
from SmartNixieTube import SmartNixieTube


class testSmartNixieTube(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SmartNixieTube_initialisation(self):
        numberOfTubesInDisplay = 3
        smartNixieTubeDisplay = SmartNixieTubeDisplay(numberOfTubesInDisplay)
        self.assertEqual(smartNixieTubeDisplay.numberOfTubesInDisplay, numberOfTubesInDisplay)

    def test_SmartNixieTube_initialisation_with_no_tubes(self):
        numberOfTubesInDisplay = 0

        try:
            self.assertRaises(AssertionError, SmartNixieTubeDisplay(numberOfTubesInDisplay))  # this should fail
            self.fail("Didn't raise AssertionError")
        except:
            pass

    def test_SmartNixieTube_initialisation_with_negative_tubes(self):
        numberOfTubesInDisplay = -1

        try:
            self.assertRaises(AssertionError, SmartNixieTubeDisplay(numberOfTubesInDisplay))  # this should fail
            self.fail("Didn't raise AssertionError")
        except:
            pass

    def test_init_digit_in_range(self):
        tube = SmartNixieTube(digit='0')
        self.assertEquals(tube.digit, '0')

    def test_init_digits_out_of_range(self):
        tube = SmartNixieTube(digit='=', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0,
                              red=0, green=0,
                              blue=0)
        self.assertEqual(tube.digit, '-')  # tube turned off if send something out of bounds.

    def test_init_digits_not_a_number(self):
        tube = SmartNixieTube(digit='A', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0,
                              red=0, green=0,
                              blue=0)
        self.assertEqual(tube.digit, '-')  # tube turned off if send something out of bounds.

    def test_init_leftDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError, SmartNixieTube(leftdecimalpoint=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual(str(e), 'Left decimal point must be of type bool')

    def test_init_rightDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError, SmartNixieTube(rightdecimalpoint=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual(str(e), 'Right decimal point must be of type bool')

    def test_init_brightness_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTube(brightness=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Brightness must be between 0-255')

        try:
            self.assertRaises(ValueError, SmartNixieTube(brightness=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Brightness must be between 0-255')

    def test_init_red_out_of_range(self):
        try:
            self.assertRaises(AssertionError, SmartNixieTube(red=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Red must be between 0-255')

        try:
            self.assertRaises(AssertionError, SmartNixieTube(red=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Red must be between 0-255')

    def test_init_blue_out_of_range(self):
        try:
            self.assertRaises(AssertionError, SmartNixieTube(blue=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Blue must be between 0-255')

        try:
            self.assertRaises(AssertionError, SmartNixieTube(blue=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Blue must be between 0-255')

    def test_init_green_out_of_range(self):
        try:
            self.assertRaises(AssertionError, SmartNixieTube(green=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Green must be between 0-255')

        try:
            self.assertRaises(AssertionError, SmartNixieTube(green=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Green must be between 0-255')

    def test_init_defaults(self):
        tube = SmartNixieTube()
        self.assertEquals(tube.digit, '-')
        self.assertEquals(tube.leftDecimalPoint, False)
        self.assertEquals(tube.rightDecimalPoint, False)
        self.assertEquals(tube.brightness, 0)
        self.assertEquals(tube.blue, 0)
        self.assertEquals(tube.green, 0)
        self.assertEquals(tube.red, 0)

    def test_convertDigitToStringWithLeadingZeros(self):
        tube = SmartNixieTube()
        self.assertEquals(tube.convertDigitToStringWithLeadingZeros(0), '000')
        self.assertEquals(tube.convertDigitToStringWithLeadingZeros(1), '001')
        self.assertEquals(tube.convertDigitToStringWithLeadingZeros(10), '010')
        self.assertEquals(tube.convertDigitToStringWithLeadingZeros(100), '100')

    def test_convertFromBoolToYN(self):
        tube = SmartNixieTube()
        self.assertEquals(tube.convertFromBooltoYN(True), 'Y')
        self.assertEquals(tube.convertFromBooltoYN(False), 'N')

    def test_generateCommandString(self):
        tube = SmartNixieTube()
        self.assertEquals(tube.generateCommandString(), '$-,N,N,000,000,000,000')

        tube2 = SmartNixieTube('9', False, False, 128, 0, 255, 255)
        self.assertEquals(tube2.generateCommandString(), '$9,N,N,128,000,255,255')

        tube3 = SmartNixieTube('5', False, False, 28, 0, 10, 1)
        self.assertEquals(tube3.generateCommandString(), '$5,N,N,028,000,010,001')

    def test_turnOff(self):
        tube = SmartNixieTube('9', False, False, 128, 0, 255, 255)
        self.assertEquals(tube.generateCommandString(), '$9,N,N,128,000,255,255')

        tube.turnOff()
        self.assertEquals(tube.generateCommandString(), '$-,N,N,000,000,000,000')


if __name__ == '__main__':
    unittest.main()
