import unittest
import time
import subprocess
import re
from os import remove
from sys import platform as _platform

try:
    from smartnixietube.SmartNixieTubeDisplay import SmartNixieTubeDisplay
except ImportError as e:
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from smartnixietube.SmartNixieTubeDisplay import SmartNixieTubeDisplay

__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'


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


if __name__ == '__main__':
    # run unit tests
    unittest.main(warnings='ignore')
