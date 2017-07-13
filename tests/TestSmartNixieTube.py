import unittest
import time
import subprocess
import re
from os import remove
from sys import platform as _platform
import serial

try:
    from smartnixietube.SmartNixieTube import SmartNixieTubeDisplay
except ImportError as e:
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from smartnixietube.SmartNixieTube import SmartNixieTubeDisplay

__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'


class TestSmartNixieTube(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_digit_in_range(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube(digit='0')
        self.assertEqual('0', tube.digit)

    def test_init_digits_out_of_range(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube(digit='=', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=0,
                                                    red=0, green=0,
                                                    blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_digits_not_a_number(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube(digit='A', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=0,
                                                    red=0, green=0,
                                                    blue=0)
        self.assertEqual('-', tube.digit)  # tube turned off if send something out of bounds.

    def test_init_leftDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError,
                              SmartNixieTubeDisplay.SmartNixieTube(left_decimal_point=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('Left decimal point must be of type bool', str(e))

    def test_init_rightDecimalPoint_wrong_type(self):
        try:
            self.assertRaises(TypeError,
                              SmartNixieTubeDisplay.SmartNixieTube(right_decimal_point=-1))  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('Right decimal point must be of type bool', str(e))

    def test_init_brightness_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(brightness=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(brightness=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

    def test_init_red_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(red=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(red=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

    def test_init_blue_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(blue=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(blue=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

    def test_init_green_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(green=-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay.SmartNixieTube(green=256))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

    def test_init_defaults(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube()
        self.assertEqual('-', tube.digit)
        self.assertEqual(False, tube.left_decimal_point)
        self.assertEqual(False, tube.right_decimal_point)
        self.assertEqual(0, tube.brightness)
        self.assertEqual(0, tube.blue)
        self.assertEqual(0, tube.green)
        self.assertEqual(0, tube.red)

    def test_convertDigitToStringWithLeadingZeros(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube()
        self.assertEqual('000', tube.convert_digit_to_string_with_leading_zeros(0))
        self.assertEqual('001', tube.convert_digit_to_string_with_leading_zeros(1))
        self.assertEqual('010', tube.convert_digit_to_string_with_leading_zeros(10))
        self.assertEqual('100', tube.convert_digit_to_string_with_leading_zeros(100))

    def test_convertFromBoolToYN(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube()
        self.assertEqual(tube.convert_from_bool_to_yn(True), 'Y')
        self.assertEqual(tube.convert_from_bool_to_yn(False), 'N')

    def test_generateCommandString(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generate_command_string())

        tube2 = SmartNixieTubeDisplay.SmartNixieTube('9', left_decimal_point=False, right_decimal_point=False,
                                                     brightness=128, red=0, green=255, blue=255)
        self.assertEqual('$9,N,N,128,000,255,255', tube2.generate_command_string())

        tube3 = SmartNixieTubeDisplay.SmartNixieTube('5', left_decimal_point=False, right_decimal_point=False,
                                                     brightness=28, red=0, green=10, blue=1)
        self.assertEqual('$5,N,N,028,000,010,001', tube3.generate_command_string())

    def test_LeftDecimalCommandString(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube(left_decimal_point=True)
        self.assertEqual('$-,Y,N,000,000,000,000', tube.generate_command_string())

    def test_RightDecimalCommandString(self):
        tube = SmartNixieTubeDisplay.SmartNixieTube(right_decimal_point=True)
        self.assertEqual('$-,N,Y,000,000,000,000', tube.generate_command_string())

    def test_turnOff(self):
        # turn on anything, check that it's on
        tube = SmartNixieTubeDisplay.SmartNixieTube('9', left_decimal_point=False, right_decimal_point=False,
                                                    brightness=128, red=0, green=255, blue=255)
        self.assertEqual('$9,N,N,128,000,255,255', tube.generate_command_string())

        # test that the generate command string sends out zeros and a dash after turn_off()
        tube.turn_off()
        self.assertEqual('$-,N,N,000,000,000,000', tube.generate_command_string())


class TestSmartNixieTubeDisplay(unittest.TestCase):
    def setUp(self):
        # Create two serial ports and connect them.
        self.socatlf = 'socat_out.txt'
        if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            args = ['socat', '-d', '-d', '-lf' + self.socatlf, 'pty,raw,echo=0', 'pty,raw,echo=0']
        elif _platform == "win32":
            # Windows...
            self.fail()

        self.socatProcess = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

        time.sleep(0.1)  # give the system a moment to actually write the socat_out file.

        # get the port names
        try:
            self.inputPort, self.outputPort = self.get_serial_ports_from_socat_output(self.socatlf)
        except ValueError as e:
            print(str(e))

    def tearDown(self):
        # kill the existing socat process so we don't have extra ports hanging around.
        self.socatProcess.kill()

        # reset output file
        remove(self.socatlf)

    def get_serial_ports_from_socat_output(self, file):
        file = open(file, 'r')  # file, readonly
        lines = []

        # get the lines with our ports in them.
        for line in file:
            if re.search('/dev/', line):
                lines.append(line)

        # print(lines)

        # there should be two lines with ports in them.
        if len(lines) == 2:
            input_port = lines[0].split()[6]
            output_port = lines[1].split()[6]
        else:
            raise ValueError('%s file malformed' % file)

        # print (input_port, output_port)

        return input_port, output_port

    def test_SmartNixieTube_initialisation(self):
        number_of_tubes_in_display = 3
        smart_nixie_tube_display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)
        self.assertEqual(smart_nixie_tube_display.number_of_tubes_in_display, number_of_tubes_in_display)

    def test_SmartNixieTubeDisplay_initialisation_with_no_tubes(self):
        number_of_tubes_in_display = 0

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('number_of_tubes_in_display must be greater than 0', str(e))

    def test_SmartNixieTubeDisplay_initialisation_with_negative_tubes(self):
        number_of_tubes_in_display = -1

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('number_of_tubes_in_display must be greater than 0', str(e))

    def test_SmartNixieTubeDisplay_init_with_one_tube(self):
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        self.assertEqual(len(display.tubes), number_of_tubes_in_display)
        self.assertEqual('$-,N,N,000,000,000,000', display.tubes[0].generate_command_string())

    def test_SmartNixieTubeDisplay_generateCommandString(self):
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        self.assertEqual('$-,N,N,000,000,000,000!', display.generate_command_string())

    def test_SmartNixieTubeDisplay_init_with_two_tubes(self):
        number_of_tubes_in_display = 2
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        self.assertEqual(len(display.tubes), number_of_tubes_in_display)
        for tube in display.tubes:
            self.assertEqual('$-,N,N,000,000,000,000', tube.generate_command_string())

    def test_SmartNixieTubeDisplay_2tubes_generateCommandString(self):
        number_of_tubes_in_display = 2
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        self.assertEqual('$-,N,N,000,000,000,000$-,N,N,000,000,000,000!', display.generate_command_string())

    def test_SmartNixieTubeDisplay_3tubes_generateCommandString(self):
        number_of_tubes_in_display = 3
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        self.assertEqual('$-,N,N,000,000,000,000$-,N,N,000,000,000,000$-,N,N,000,000,000,000!',
                         display.generate_command_string())

    def test_SmartNixieTubeDisplay_3tubes_nonDefault_generateCommandString(self):
        number_of_tubes_in_display = 3
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.tubes[0].digit = '0'
        display.tubes[1].digit = '1'
        display.tubes[2].digit = '2'

        self.assertEqual('$2,N,N,000,000,000,000$1,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display.generate_command_string())

    def test_SmartNixieTubeDisplay_set_display_numbers_out_of_bounds(self):
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        try:
            self.assertRaises(ValueError, display.set_display_number(-1))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Display number must be positive')

        try:
            self.assertRaises(ValueError, display.set_display_number(10))  # this should fail (too many digits)
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual(str(e), 'Not enough tubes to display all digits')

    def test_SmartNixieTubeDisplay_set_one_tube_display_numbers(self):
        # set one tube
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.set_display_number(9)
        self.assertEqual('$9,N,N,000,000,000,000!', display.generate_command_string())

    def test_SmartNixieTubeDisplay_set_two_tube_display_numbers(self):
        # set two tubes
        number_of_tubes_in_display = 2
        display2 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display2.set_display_number(9)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000!', display2.generate_command_string())

        display2.set_display_number(90)
        self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000!', display2.generate_command_string())

        display2.set_display_number(99)
        self.assertEqual('$9,N,N,000,000,000,000$9,N,N,000,000,000,000!', display2.generate_command_string())

    def test_SmartNixieTubeDisplay_set_three_tube_display_numbers(self):
        # set three tubes
        number_of_tubes_in_display = 3
        display3 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display3.set_display_number(9)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display3.generate_command_string())

        display3.set_display_number(99)
        self.assertEqual('$9,N,N,000,000,000,000$9,N,N,000,000,000,000$0,N,N,000,000,000,000!',
                         display3.generate_command_string())

        display3.set_display_number(909)
        self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$9,N,N,000,000,000,000!',
                         display3.generate_command_string())

        display3.set_display_number(990)
        self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000$9,N,N,000,000,000,000!',
                         display3.generate_command_string())

    def test_init_display_brightness_out_of_range(self):
        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(number_of_tubes_in_display=1, brightness=-1,
                                                    serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(number_of_tubes_in_display=1, brightness=256,
                                                    serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Brightness must be between 0-255', str(e))

    def test_init_display_red_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display=1, red=-1,
                                                                serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display=1, red=256,
                                                                serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Red must be between 0-255', str(e))

    def test_init_display_blue_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display=1, blue=-1,
                                                                serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display=1, blue=256,
                                                                serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Blue must be between 0-255', str(e))

    def test_init_display_green_out_of_range(self):
        try:
            self.assertRaises(ValueError, SmartNixieTubeDisplay(number_of_tubes_in_display=1, green=-1,
                                                                serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

        try:
            self.assertRaises(ValueError,
                              SmartNixieTubeDisplay(number_of_tubes_in_display=1, green=256,
                                                    serial_port_name=self.inputPort))  # this should fail
            self.fail("Didn't raise ValueError")
        except ValueError as e:
            self.assertEqual('Green must be between 0-255', str(e))

    def test_init_display_brightness(self):
        # set one tube
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000!', display.generate_command_string())

        # set two tubes
        number_of_tubes_in_display = 2
        tube_display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)
        display2 = tube_display

        display2.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000$-,N,N,128,000,000,000!', display2.generate_command_string())

        # set three tubes
        number_of_tubes_in_display = 3
        display3 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display3.brightness = 128
        self.assertEqual('$-,N,N,128,000,000,000$-,N,N,128,000,000,000$-,N,N,128,000,000,000!',
                         display3.generate_command_string())

    def test_init_display_red(self):
        # set one tube
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.red = 128
        self.assertEqual('$-,N,N,000,128,000,000!', display.generate_command_string())

        # set two tubes
        number_of_tubes_in_display = 2
        display2 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display2.red = 128
        self.assertEqual('$-,N,N,000,128,000,000$-,N,N,000,128,000,000!', display2.generate_command_string())

        # set three tubes
        number_of_tubes_in_display = 3
        display3 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display3.red = 128
        self.assertEqual('$-,N,N,000,128,000,000$-,N,N,000,128,000,000$-,N,N,000,128,000,000!',
                         display3.generate_command_string())

    def test_init_display_green(self):
        # set one tube
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.green = 128
        self.assertEqual('$-,N,N,000,000,128,000!', display.generate_command_string())

        # set two tubes
        number_of_tubes_in_display = 2
        display2 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display2.green = 128
        self.assertEqual('$-,N,N,000,000,128,000$-,N,N,000,000,128,000!', display2.generate_command_string())

        # set three tubes
        number_of_tubes_in_display = 3
        display3 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display3.green = 128
        self.assertEqual('$-,N,N,000,000,128,000$-,N,N,000,000,128,000$-,N,N,000,000,128,000!',
                         display3.generate_command_string())

    def test_init_display_blue(self):
        # set one tube
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128!', display.generate_command_string())

        # set two tubes
        number_of_tubes_in_display = 2
        display2 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display2.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128$-,N,N,000,000,000,128!', display2.generate_command_string())

        # set three tubes
        number_of_tubes_in_display = 3
        display3 = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.inputPort)

        display3.blue = 128
        self.assertEqual('$-,N,N,000,000,000,128$-,N,N,000,000,000,128$-,N,N,000,000,000,128!',
                         display3.generate_command_string())


class TestSmartNixieTubeDisplaySerialConnections(unittest.TestCase):
    def setUp(self):
        # Create two serial ports and connect them.
        self.socatlf = 'socat_out.txt'
        if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            args = ['socat', '-d', '-d', '-lf' + self.socatlf, 'pty,raw,echo=0', 'pty,raw,echo=0']
        elif _platform == "win32":
            # Windows...
            self.fail()

        self.socatProcess = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

        time.sleep(0.1)  # give the system a moment to actually write the socat_out file.

        # get the port names
        try:
            self.input_port, self.output_port = self.get_serial_ports_from_socat_output(self.socatlf)
        except ValueError as e:
            print(str(e))

    def tearDown(self):
        # kill the existing socat process so we don't have extra ports hanging around.
        self.socatProcess.kill()

        # reset output file
        remove(self.socatlf)

    def get_serial_ports_from_socat_output(self, file):
        file = open(file, 'r')  # file, readonly
        lines = []

        # get the lines with our ports in them.
        for line in file:
            if re.search('/dev/', line):
                lines.append(line)

        # there should be two lines with ports in them.
        if len(lines) == 2:
            input_port = lines[0].split()[6]
            output_port = lines[1].split()[6]
        else:
            raise ValueError('%s file malformed' % file)

        return input_port, output_port

    def test_socat_serial_names_from_sample_output(self):
        # read the socat sample output file
        # test_socat_out_sample

        try:
            input_port, output_port = self.get_serial_ports_from_socat_output('test_socat_out_sample')
        except ValueError as e:
            pass

        # get the two port names /dev/ttys046 and /dev/ttys047
        self.assertEqual('/dev/ttys046', input_port)
        self.assertEqual('/dev/ttys047', output_port)

    def test_communication_between_socat_com_ports(self):
        write_to_port = serial.Serial(
            port=self.output_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        message_out = 'hello, world!\n'
        if write_to_port.isOpen() and read_from_port.isOpen():
            write_to_port.write(message_out.encode())
            message_in = read_from_port.readline(20)
            self.assertEqual(message_out.encode(), message_in)
        else:
            self.fail('Serial ports failed to open')

        write_to_port.close()
        read_from_port.close()

    def test_command_string_between_socat_com_ports(self):
        write_to_port = serial.Serial(
            port=self.output_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        message_out = '$-,N,N,000,000,000,000!'
        if write_to_port.isOpen():
            write_to_port.write(message_out.encode())
        else:
            self.fail('write_to_port failed to open')

        if read_from_port.isOpen():
            last_received = b''
            buffer_string = b''
            while last_received != b'!':
                last_received = read_from_port.readline(1)
                buffer_string = buffer_string + last_received
                if b'!' in buffer_string:
                    self.assertEqual(message_out.encode(), buffer_string)
        else:
            self.fail('read_from_port failed to open')

        write_to_port.close()
        read_from_port.close()

    def test_long_command_string_between_socat_com_ports(self):
        write_to_port = serial.Serial(
            port=self.output_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        message_out = '$-,N,N,000,000,000,000$-,N,N,000,000,000,000$-,N,N,000,000,000,000$-,N,N,000,000,000,000!'
        if write_to_port.isOpen():
            write_to_port.write(message_out.encode())
        else:
            self.fail('write_to_port failed to open')

        if read_from_port.isOpen():
            last_received = b''
            buffer_string = b''
            while last_received != b'!':
                last_received = read_from_port.readline(1)
                buffer_string = buffer_string + last_received
                if b'!' in buffer_string:
                    self.assertEqual(message_out.encode(), buffer_string)
        else:
            self.fail('read_from_port failed to open')

        read_from_port.close()
        write_to_port.close()

    def test_init_serialPort(self):
        try:
            self.assertRaises(TypeError, SmartNixieTubeDisplay(1, serial_port_name=-1), shell=True)  # this should fail
            self.fail("Didn't raise TypeError")
        except TypeError as e:
            self.assertEqual('serialPort must be of type str', str(e))

    def test_sendCommand_1tubes_nonDefault(self):
        number_of_tubes_in_display = 1
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.output_port)

        display.set_display_number(9)
        # this should equal: '$9,N,N,000,000,000,000!'

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        display.send_command()

        if read_from_port.isOpen():
            last_received = b''
            buffer_string = b''
            while last_received != b'!':
                last_received = read_from_port.readline(1)
                # print(last_received)
                buffer_string = buffer_string + last_received
                if b'!' in buffer_string:
                    # print(buffer_string)
                    self.assertEqual('$9,N,N,000,000,000,000!'.encode()
                                     , buffer_string)
        else:
            self.fail('read_from_port failed to open')

        read_from_port.close()

    def test_sendCommand_2tubes_nonDefault(self):
        number_of_tubes_in_display = 2
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.output_port)

        display.set_display_number(90)
        # this should equal: '$0,N,N,000,000,000,000$9,N,N,000,000,000,000!'

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        display.send_command()

        if read_from_port.isOpen():
            last_received = b''
            buffer_string = b''
            while last_received != b'!':
                last_received = read_from_port.readline(1)
                # print(last_received)
                buffer_string = buffer_string + last_received
                if b'!' in buffer_string:
                    # print(buffer_string)
                    self.assertEqual('$0,N,N,000,000,000,000$9,N,N,000,000,000,000!'.encode()
                                     , buffer_string)
        else:
            self.fail('read_from_port failed to open')

        read_from_port.close()

    def test_sendCommand_3tubes_nonDefault(self):
        number_of_tubes_in_display = 3
        display = SmartNixieTubeDisplay(number_of_tubes_in_display, serial_port_name=self.output_port)

        display.set_display_number(909)
        # this should equal: '$9,N,N,000,000,000,000$0,N,N,000,000,000,000$9,N,N,000,000,000,000!'

        read_from_port = serial.Serial(
            port=self.input_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        display.send_command()

        if read_from_port.isOpen():
            last_received = b''
            buffer_string = b''
            while last_received != b'!':
                last_received = read_from_port.readline(1)
                # print(last_received)
                buffer_string = buffer_string + last_received
                if b'!' in buffer_string:
                    # print(buffer_string)
                    self.assertEqual('$9,N,N,000,000,000,000$0,N,N,000,000,000,000$9,N,N,000,000,000,000!'.encode()
                                     , buffer_string)
        else:
            self.fail('read_from_port failed to open')

        read_from_port.close()


if __name__ == '__main__':
    # run unit tests
    unittest.main(warnings='ignore')
