__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

from subprocess import *

from Adafruit_CharLCD import Adafruit_CharLCD


def run_cmd(cmd):
    p = Popen(cmd, shell = True, stdout = PIPE)
    output = p.communicate()[0]
    return output


def main():
    """main"""
    lcd = Adafruit_CharLCD()
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"  # get the device ip address

    # LCD setup
    lcd.begin(16, 2)

    lcd.clear()
    ipaddress = run_cmd(cmd)

    lcd.message('wlan0 IP Address\n')
    lcd.message('%s' % ipaddress)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt.")
