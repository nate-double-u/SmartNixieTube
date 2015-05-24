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

    def test_init_digit_in_range(self):
        tube = SmartNixieTube(digit='0')
        self.assertEqual('0', tube.digit)

    def test_init_digits_out_of_range(self):
        tube = SmartNixieTube(digit='=', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0,
                              red=0, green=0,
                              blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_digits_not_a_number(self):
        tube = SmartNixieTube(digit='A', leftdecimalpoint=False, rightdecimalpoint=False, brightness=0,
                              red=0, green=0,
                              blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_leftDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError, SmartNixieTube(leftdecimalpoint=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('Left decimal point must be of type bool', str(e))

    def test_init_rightDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError, SmartNixieTube(rightdecimalpoint=-1))  # this should fail
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
        self.assertEqual(False, tube.leftDecimalPoint)
        self.assertEqual(False, tube.rightDecimalPoint)
        self.assertEqual(0, tube.brightness)
        self.assertEqual(0, tube.blue)
        self.assertEqual(0, tube.green)
        self.assertEqual(0, tube.red)

    def test_convertDigitToStringWithLeadingZeros(self):
        tube = SmartNixieTube()
        self.assertEqual('000', tube.convertDigitToStringWithLeadingZeros(0))
        self.assertEqual('001', tube.convertDigitToStringWithLeadingZeros(1))
        self.assertEqual('010', tube.convertDigitToStringWithLeadingZeros(10))
        self.assertEqual('100', tube.convertDigitToStringWithLeadingZeros(100))

    def test_convertFromBoolToYN(self):
        tube = SmartNixieTube()
        self.assertEqual(tube.convertFromBooltoYN(True), 'Y')
        self.assertEqual(tube.convertFromBooltoYN(False), 'N')

    def test_generateCommandString(self):
        tube = SmartNixieTube()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generateCommandString())

        tube2 = SmartNixieTube('9', False, False, 128, 0, 255, 255)
        self.assertEqual('$9,N,N,128,000,255,255', tube2.generateCommandString())

        tube3 = SmartNixieTube('5', False, False, 28, 0, 10, 1)
        self.assertEqual('$5,N,N,028,000,010,001', tube3.generateCommandString())

    def test_LeftDecimalCommandString(self):
        tube = SmartNixieTube(leftdecimalpoint=True)
        self.assertEqual('$-,Y,N,000,000,000,000', tube.generateCommandString())

    def test_RightDecimalCommandString(self):
        tube = SmartNixieTube(rightdecimalpoint=True)
        self.assertEqual('$-,N,Y,000,000,000,000', tube.generateCommandString())

    def test_turnOff(self):
        # turn on anything, check that it's on
        tube = SmartNixieTube('9', False, False, 128, 0, 255, 255)
        self.assertEqual('$9,N,N,128,000,255,255', tube.generateCommandString())

        # test that the generate command string sends out zeros and a dash after turnOff()
        tube.turnOff()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generateCommandString())


class testSmartNixieTubeDisplay(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SmartNixieTube_initialisation(self):
        numberOfTubesInDisplay = 3
        smartNixieTubeDisplay = SmartNixieTubeDisplay(numberOfTubesInDisplay)
        self.assertEqual(smartNixieTubeDisplay.numberOfTubesInDisplay, numberOfTubesInDisplay)

    def test_SmartNixieTubeDisplay_initialisation_with_no_tubes(self):
        numberOfTubesInDisplay = 0

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('numberOfTubesInDisplay must be greater than 0', str(e))

    def test_SmartNixieTubeDisplay_initialisation_with_negative_tubes(self):
        numberOfTubesInDisplay = -1

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('numberOfTubesInDisplay must be greater than 0', str(e))

    def test_SmartNixieTubeDisplay_init_with_one_tube(self):
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEqual(len(display.tubes), numberOfTubesInDisplay)
        self.assertEqual('$-,N,N,000,000,000,000', display.tubes[0].generateCommandString())

    def test_SmartNixieTubeDisplay_generateCommandString(self):
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEqual('$-,N,N,000,000,000,000!', display.generateCommandString())

    def test_SmartNixieTubeDisplay_init_with_two_tubes(self):
        numberOfTubesInDisplay = 2
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEqual(len(display.tubes), numberOfTubesInDisplay)
        for tube in display.tubes:
            self.assertEqual('$-,N,N,000,000,000,000', tube.generateCommandString())

    def test_SmartNixieTubeDisplay_2tubes_generateCommandString(self):
        numberOfTubesInDisplay = 2
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEqual('$-,N,N,000,000,000,000$-,N,N,000,000,000,000!', display.generateCommandString())

    def test_SmartNixieTubeDisplay_3tubes_generateCommandString(self):
        numberOfTubesInDisplay = 3
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEqual('$-,N,N,000,000,000,000$-,N,N,000,000,000,000$-,N,N,000,000,000,000!',
                         display.generateCommandString())

    def test_SmartNixieTubeDisplay_3tubes_nonDefault_generateCommandString(self):
        numberOfTubesInDisplay = 3
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.tubes[0].digit = '0'
        display.tubes[1].digit = '1'
        display.tubes[2].digit = '2'

        self.assertEqual('$2,N,N,000,000,000,000$1,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display.generateCommandString())

    def test_SmartNixieTubeDisplay_set_display_numbers_out_of_bounds(self):
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        try:
            self.assertRaises(ValueError, display.setDisplayNumber(-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Display number must be positive')

        try:
            self.assertRaises(ValueError, display.setDisplayNumber(10))  # this should fail (too many digits)
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Not enough tubes to display all digits')

    def test_SmartNixieTubeDisplay_set_one_tube_display_numbers(self):
        # set one tube
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.setDisplayNumber(9)
        self.assertEqual('$9,N,N,000,000,000,000!', display.generateCommandString())

    def test_SmartNixieTubeDisplay_set_two_tube_display_numbers(self):
        # set two tubes
        numberOfTubesInDisplay = 2
        display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display2.setDisplayNumber(9)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000!', display2.generateCommandString())

        display2.setDisplayNumber(90)
        self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000!', display2.generateCommandString())

        display2.setDisplayNumber(99)
        self.assertEqual('$9,N,N,000,000,000,000$9,N,N,000,000,000,000!', display2.generateCommandString())

    def test_SmartNixieTubeDisplay_set_three_tube_display_numbers(self):
        # set three tubes
        numberOfTubesInDisplay = 3
        display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display3.setDisplayNumber(9)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display3.generateCommandString())

        display3.setDisplayNumber(99)
        self.assertEqual('$9,N,N,000,000,000,000$9,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display3.generateCommandString())

        display3.setDisplayNumber(909)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$9,N,N,000,000,000,000!',
                         display3.generateCommandString())

        display3.setDisplayNumber(990)
        self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000$9,N,N,000,000,000,000!',
                         display3.generateCommandString())

    # def test_SmartNixieTubeDisplay_set_too_many_digits_with_decimals(self):
    #     numberOfTubesInDisplay = 1
    #     display = SmartNixieTubeDisplay(numberOfTubesInDisplay)
    #     try:
    #         self.assertRaises(ValueError, display.setDisplayNumber(9.0))  # this should fail (too many digits)
    #         self.fail("Didn't raise ValueError")
    #     except ValueError as e:
    #         self.assertEqual(str(e), 'Not enough tubes to display all digits')
    #
    # def test_SmartNixieTubeDisplay_set_one_tube_display_numbers_with_decimals(self):
    #     # set one tube
    #     numberOfTubesInDisplay = 1
    #     display = SmartNixieTubeDisplay(numberOfTubesInDisplay)
    #
    #     display.setDisplayNumber(0.9)
    #     self.assertEqual('$9,Y,N,000,000,000,000!', display.generateCommandString())
    #
    #
    # def test_SmartNixieTubeDisplay_set_two_tube_display_numbers_with_decimals(self):
    #     # set two tubes
    #     numberOfTubesInDisplay = 2
    #     display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)
    #
    #     display2.setDisplayNumber(0.9)
    #     self.assertEqual('$9,Y,N,000,000,000,000$0,N,N,000,000,000,000!', display2.generateCommandString())
    #
    #     display2.setDisplayNumber(0.99)
    #     self.assertEqual('$9,Y,N,000,000,000,000$9,N,N,000,000,000,000!', display2.generateCommandString())
    #
    #     display2.setDisplayNumber(9.9)
    #     self.assertEqual('$9,N,N,000,000,000,000$9,Y,N,000,000,000,000!', display2.generateCommandString())
    #
    # def test_SmartNixieTubeDisplay_set_three_tube_display_numbers_with_decimals(self):
    #     # set three tubes
    #     numberOfTubesInDisplay = 3
    #     display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)
    #
    #     display3.setDisplayNumber(0.9)
    #     self.assertEqual('$9,Y,N,000,000,000,000$0,N,N,000,000,000,000$0,N,N,000,000,000,000!',
    #                      display3.generateCommandString())
    #
    #     display3.setDisplayNumber(99)
    #     self.assertEqual('$9,N,N,000,000,000,000$9,N,N,000,000,000,000$0,N,N,000,000,000,000!',
    #                      display3.generateCommandString())
    #
    #     display3.setDisplayNumber(909)
    #     self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$9,N,N,000,000,000,000!',
    #                      display3.generateCommandString())
    #
    #     display3.setDisplayNumber(990)
    #     self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000$9,N,N,000,000,000,000!',
    #                      display3.generateCommandString())

    def test_init_display_brightness_out_of_range(self):
        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(numberOfTubesInDisplay=1, brightness=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(numberOfTubesInDisplay=1, brightness=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

    def test_init_display_red_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay=1, red=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay=1, red=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

    def test_init_display_blue_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay=1, blue=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay=1, blue=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

    def test_init_display_green_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(numberOfTubesInDisplay=1, green=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(numberOfTubesInDisplay=1, green=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

    def test_init_display_brightness(self):
        # set one tube
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000!', display.generateCommandString())

        # set two tubes
        numberOfTubesInDisplay = 2
        display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display2.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000$-,N,N,128,000,000,000!', display2.generateCommandString())

        # set three tubes
        numberOfTubesInDisplay = 3
        display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display3.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000$-,N,N,128,000,000,000$-,N,N,128,000,000,000!',
                         display3.generateCommandString())

    def test_init_display_red(self):
        # set one tube
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.red = 128
        self.assertEqual('$-,N,N,000,128,000,000!', display.generateCommandString())

        # set two tubes
        numberOfTubesInDisplay = 2
        display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display2.red = 128
        self.assertEqual('$-,N,N,000,128,000,000$-,N,N,000,128,000,000!', display2.generateCommandString())

        # set three tubes
        numberOfTubesInDisplay = 3
        display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display3.red = 128
        self.assertEqual('$-,N,N,000,128,000,000$-,N,N,000,128,000,000$-,N,N,000,128,000,000!',
                         display3.generateCommandString())

    def test_init_display_green(self):
        # set one tube
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.green = 128
        self.assertEqual('$-,N,N,000,000,128,000!', display.generateCommandString())

        # set two tubes
        numberOfTubesInDisplay = 2
        display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display2.green = 128
        self.assertEqual('$-,N,N,000,000,128,000$-,N,N,000,000,128,000!', display2.generateCommandString())

        # set three tubes
        numberOfTubesInDisplay = 3
        display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display3.green = 128
        self.assertEqual('$-,N,N,000,000,128,000$-,N,N,000,000,128,000$-,N,N,000,000,128,000!',
                         display3.generateCommandString())

    def test_init_display_blue(self):
        # set one tube
        numberOfTubesInDisplay = 1
        display = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128!', display.generateCommandString())

        # set two tubes
        numberOfTubesInDisplay = 2
        display2 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display2.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128$-,N,N,000,000,000,128!', display2.generateCommandString())

        # set three tubes
        numberOfTubesInDisplay = 3
        display3 = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        display3.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128$-,N,N,000,000,000,128$-,N,N,000,000,000,128!',
                         display3.generateCommandString())

    # Testing serial port...
    def test_init_serialPort(self):
        try:
            self.assertRaises(TypeError, SmartNixieTubeDisplay(1, serialPort=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('serialPort must be of type str', str(e))


if __name__ == '__main__':
    # unit tests
    unittest.main()
