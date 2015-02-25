__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

from subprocess import *
from time import sleep
import socket
import sys
import struct
import ctypes
import ctypes.util
import time
import datetime
import json

from firebase import firebase
from dateutil import parser

import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD


DEBUG = True

# Time Stuff
nistHostName = 'time.nist.gov'
nistPort = 37

nistHost = socket.gethostbyname(nistHostName)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('', (nistHost, nistPort))

BLU_PIN = 23  # no.8


class CoffeeCounter(object):
    _machineId = '1'
    _dailyCoffeeCount = 0
    _currentDay = 0
    _lcd = Adafruit_CharLCD()
    _ledOn = False
    _timer = 0;

    def __init__(self):
        """this is the set-up phase, get things ready!"""

        # Time stuff
        currentNistTime = self._getNistTime()  # what time is it? (officially)
        self._currentDay = currentNistTime.day

        time_tuple = ( currentNistTime.year,
                       currentNistTime.month,
                       currentNistTime.day,
                       currentNistTime.hour,
                       currentNistTime.minute,
                       currentNistTime.second,
                       0,  # millisecond
        )

        self._set_system_time(time_tuple)  # we have NIST time so set the system clock so we don't have to ask again.

        # light sensor setup # no.7
        GPIO.setup(BLU_PIN, GPIO.OUT)

        # Boot info
        cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"  # get the device ip address

        # LCD setup
        self._lcd.begin(16, 2)

        self._lcd.clear()
        ipaddr = self._run_cmd(cmd)

        self._lcd.message('AKQA JavaCounter\n')
        self._lcd.message('IP %s' % (ipaddr))

        # sleep(5)
        self._lcd.setCursor(0, 1)
        self._lcd.message('                ')  # clear the 2nd line for the counter

        # setup backend
        self.__firebase = firebase.FirebaseApplication('https://amber-torch-2593.firebaseio.com/', None)

    def _set_system_time(self, time_tuple):

        # /usr/include/linux/time.h:
        #
        # define CLOCK_REALTIME                     0
        CLOCK_REALTIME = 0

        # /usr/include/time.h
        #
        # struct timespec
        # {
        # __time_t tv_sec;            /* Seconds.  */
        # long int tv_nsec;           /* Nanoseconds.  */
        # };
        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple()))
        ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

    def _getNistTime(self):
        if DEBUG:
            print "Looking for replies."
        buf = s.recvfrom(2048)[0]
        if len(buf) != 4:
            print 'len(buf) != 4'
            if DEBUG:
                print "Wrong-sized reply %d: %s" % (len(buf), buf)
            sys.exit(1)  # TODO: Handle this exception better

        secs = struct.unpack("!I", buf)[0]
        secs -= 2208988800

        dateString = time.ctime(int(secs))
        if DEBUG:
            print dateString

        return parser.parse(dateString)


    def _msr_time(self, msr_pin):  # no.6
        # reading = 0
        # GPIO.setup(msr_pin, GPIO.OUT)
        # GPIO.output(msr_pin, GPIO.LOW)
        # time.sleep(0.1)
        # starttime = time.time()  # note start time
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(msr_pin, GPIO.IN)
        # while (GPIO.input(msr_pin) == GPIO.LOW):
        #     reading += 1
        # endtime = time.time()  # note end time
        # total_time = 1000 * (endtime - starttime)
        # return total_time  # reading in milliseconds
        return GPIO.input(msr_pin)


    def _run_cmd(self, cmd):
        p = Popen(cmd, shell = True, stdout = PIPE)
        output = p.communicate()[0]
        return output

    def _getIRSensorValue(self):  # no.5


        return self._msr_time(BLU_PIN)

    def incrementDailyCoffeeCount(self):
        if self._currentDay == datetime.datetime.now().day:
            if DEBUG:
                print "self.__dailyCoffeeCount += 1"
            self._dailyCoffeeCount += 1

        else:
            if DEBUG:
                print "self.__dailyCoffeeCount = 1"
            self._dailyCoffeeCount = 1  # would  be zero, but this is the first coffee of the day!
            self._currentDay = datetime.datetime.now().day

    def loop(self):
        """this is the main loop--runs forever."""
        while True:  # Go!

            # what's the sensor telling us # no.1
            irSensorVal = 0  # self._getIRSensorValue()

            # Set the display
            self._lcd.setCursor(0, 1)
            if DEBUG:
                self._lcd.message('{:.3f} Count {:d}\n'.format(irSensorVal, self._dailyCoffeeCount))  # no.2
            else:
                self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))

            # # count the coffees! (check for the light, and increment the counter when it goes off. # no.3
            # if irSensorVal == 1:
            #
            #     # light on, wait till it goes off to add 1 to the daily coffee count
            #     # self._lcd.setCursor(0, 1)
            #     # if DEBUG:
            #     #     self._lcd.message('{:.3f} Count {:d}\n'.format(irSensorVal, self._dailyCoffeeCount))
            #     # else:
            #     #     self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))
            #     self._timer += 1
            # else:
            #     self._timer = 0
            #
            # if self._timer == 0 and not self._ledOn:
            #     self._ledOn = True
            #     self.incrementDailyCoffeeCount()
            #
            # self._lcd.setCursor(0, 1)
            # if DEBUG:
            #     self._lcd.message('{:.3f} Count {:d}\n'.format(irSensorVal, self._dailyCoffeeCount))  # no.4
            # else:
            #     self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))
            #
            # # send the info to the backend
            timestamp = str(datetime.datetime.now())

            coffeeJson = json.dumps(
                {
                    "total": self._dailyCoffeeCount,
                    "id": self._machineId,
                    "timestamp": timestamp
                }
            )

            result = self.__firebase.post('/coffee', coffeeJson)
            if DEBUG:
                print result

            # give the system some time before the next goround
            sleep(0.3)

            if self._timer > 100:
                self._ledOn = False


def main():
    """main"""

    coffeecounter = CoffeeCounter()
    coffeecounter.loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt.")
        GPIO.cleanup()
