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
import math
import json

from firebase import firebase
from dateutil import parser

import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD


DEBUG = False

# Time Stuff
nistHostName = 'time.nist.gov'
nistPort = 37

nistHost = socket.gethostbyname(nistHostName)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('', (nistHost, nistPort))

# Define GPIO to use on Pi
GPIO_TRIGGER = 22
GPIO_ECHO = 27


class CoffeeCounter(object):
    _machineId = '1'
    _dailyCoffeeCount = 0
    _currentDay = 0
    _lcd = Adafruit_CharLCD()
    _cupPresent = False
    _timer = 0

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

        # setup GPIO stuff

        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Set pins as output and input
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_ECHO, GPIO.IN)      # Echo

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

    def _run_cmd(self, cmd):
        p = Popen(cmd, shell = True, stdout = PIPE)
        output = p.communicate()[0]
        return output

    def _getSensorValue(self):  # no.5
        # Set trigger to False (Low)
        GPIO.output(GPIO_TRIGGER, False)

        # Allow module to settle
        time.sleep(0.5)

        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance /= 5.4
        print "Ultrasonic Measurement: " + str(distance) + " inch"
        return distance

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
            sensorVal = self._getSensorValue()

            # Set the display
            self._lcd.setCursor(0, 1)
            if DEBUG:
                self._lcd.message('{:.3f} Count {:d}\n'.format(sensorVal, self._dailyCoffeeCount))
            else:
                self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))

            # count the coffees! (check for the light, and increment the counter when it goes off.
            if self._cupPresent and sensorVal > 5:
                self.incrementDailyCoffeeCount()

                #send the info to the backend
                timestamp = str(datetime.datetime.now())

                # coffeeJson = json.dumps(
                #     {
                #         'total': self._dailyCoffeeCount,
                #         'id': self._machineId,
                #         'timestamp': timestamp
                #     }
                # )

                coffeeJson = {'total': self._dailyCoffeeCount,
                              'id': self._machineId,
                              'timestamp': timestamp}

                result = self.__firebase.post('/coffee', coffeeJson)
                if DEBUG:
                    print result

            if sensorVal < 5:
                self._cupPresent = True
            else:
                self._cupPresent = False

            self._lcd.setCursor(0, 1)
            if DEBUG:
                self._lcd.message('{:.3f} Count {:d}\n'.format(sensorVal, self._dailyCoffeeCount))
            else:
                self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))



            # give the system some time before the next goround
            sleep(0.1)




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
