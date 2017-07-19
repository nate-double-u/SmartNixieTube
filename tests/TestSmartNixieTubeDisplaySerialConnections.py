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
