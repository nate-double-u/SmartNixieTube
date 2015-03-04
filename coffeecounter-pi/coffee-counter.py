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
import operator
import math
import json

from multiprocessing import Pool
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
GPIO_TRIGGER_1 = 22
GPIO_ECHO_1 = 27

GPIO_TRIGGER_2 = 17
GPIO_ECHO_2 = 4

TIMEOUT = 10


class CoffeeCounter(object):
    _dailyCoffeeCount = 0
    _dailyCoffeeCount_1 = 0
    _dailyCoffeeCount_2 = 0
    _totalCoffeeCount = 0
    _currentDay = 0
    _lcd = Adafruit_CharLCD()
    _cupPresent_1 = False
    _cupPresent_2 = False
    _timer_1 = 0
    _timer_2 = 0
    _objHr = {}
    _reset = False

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
        obj = self.__firebase.get('/coffee', None)
        # obj = sorted(obj, key=lambda x: x.timestamp, reverse=False)
        if obj is None:
            self._totalCoffeeCount = 0
        else:
            self._totalCoffeeCount = len(obj)


        #send the info to the backend
        timestamp = str(datetime.datetime.now())

                # coffeeJson = json.dumps(
                #     {
                #         'total': self._dailyCoffeeCount,
                #         'id': self._machineId,
                #         'timestamp': timestamp
                #     }
                # )

        coffeeJson = {'daily': self._dailyCoffeeCount,
                      'id': '1',
                      'timestamp': timestamp,
                      'total': self._totalCoffeeCount
                      }

        result = self.__firebase.post('/coffee', coffeeJson)
        if DEBUG:
            print result
        # print obj
        # obj_last = (obj.keys()[len(obj)-1])
        # self._dailyCoffeeCount = obj[obj_last]['total']

        # print obj[obj_last]['total']
        # setup GPIO stuff

        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Set pins as output and input
        GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_ECHO_1, GPIO.IN)      # Echo
        GPIO.setup(GPIO_ECHO_2, GPIO.IN)      # Echo

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

    def _getSensorValue(self, id_num):
        # Set trigger to False (Low)
        if id_num == 1:
            trigger = GPIO_TRIGGER_1
            echo = GPIO_ECHO_1
        elif id_num == 2:
            trigger = GPIO_TRIGGER_2
            echo = GPIO_ECHO_2

        GPIO.output(trigger, False)

        # Allow module to settle
        time.sleep(0.5)

        stop = 0

        # Send 10us pulse to trigger
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        start = time.time()

        while GPIO.input(echo) == 0:
            start = time.time()

        while GPIO.input(echo) == 1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance /= 5.4
        print "Coffee Machine #"+str(id_num)+": " + str(distance) + " inch"
        return distance

    def incrementDailyCoffeeCount(self, id_num):
        if self._currentDay == datetime.datetime.now().day:
            if DEBUG:
                print "self.__dailyCoffeeCount += 1"
            self._dailyCoffeeCount += 1
            self._totalCoffeeCount += 1
            if id_num == 1:
                self._dailyCoffeeCount_1 += 1
            elif id_num == 2:
                self._dailyCoffeeCount_2 += 1
        else:
            if DEBUG:
                print "self.__dailyCoffeeCount = 1"
            self._dailyCoffeeCount = 1  # would  be zero, but this is the first coffee of the day!
            self._currentDay = datetime.datetime.now().day

    def loop(self):
        """this is the main loop--runs forever."""
        while True:  # Go!

            # what's the sensor telling us
            sensorVal_1 = self._getSensorValue(1)
            sensorVal_2 = self._getSensorValue(2)

            # # Set the display
            # self._lcd.setCursor(0, 1)
            # if DEBUG:
            #     self._lcd.message('{:.3f} Count {:d}\n'.format(sensorVal, self._dailyCoffeeCount))
            # else:
            #     self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))

            if datetime.datetime.now().minute == 0 and self._reset is False:
                self._dailyCoffeeCount_2 = self._dailyCoffeeCount_1 = 0
                self._reset = True
            if self._reset is True:
                if datetime.datetime.now().minute == 1:
                    self._reset = False

            #count the coffees! (check for the light, and increment the counter when it goes off.
            if self._cupPresent_1 and (sensorVal_1 > 5 or sensorVal_1 < 2.5) and self._timer_1 > TIMEOUT:
                self.incrementDailyCoffeeCount(1)

                #send the info to the backend
                timestamp = str(datetime.datetime.now())
                hr = str(datetime.datetime.now().hour)
                # coffeeJson = json.dumps(
                #     {
                #         'total': self._dailyCoffeeCount,
                #         'id': self._machineId,
                #         'timestamp': timestamp
                #     }
                # )
                self._objHr[hr] = str(self._dailyCoffeeCount_1)+','+str(self._dailyCoffeeCount_2)
                coffeeJson = {'daily': self._dailyCoffeeCount,
                              'hourly': self._objHr,
                              'id': '1',
                              'timestamp': timestamp,
                              'total': self._totalCoffeeCount
                              }

                result = self.__firebase.post('/coffee', coffeeJson)
                if DEBUG:
                    print result

            if 2.5 < sensorVal_1 < 5:
                self._cupPresent_1 = True
                self._timer_1 += 1
            else:
                self._cupPresent_1 = False
                self._timer_1 = 0

            if self._cupPresent_2 and (sensorVal_2 > 5 or sensorVal_2 < 2.5) and self._timer_2 > TIMEOUT:
                self.incrementDailyCoffeeCount(2)

                #send the info to the backend
                timestamp = str(datetime.datetime.now())
                hr = str(datetime.datetime.now().hour)
                # coffeeJson = json.dumps(
                #     {
                #         'total': self._dailyCoffeeCount,
                #         'id': self._machineId,
                #         'timestamp': timestamp
                #     }
                # )
                self._objHr[hr] = str(self._dailyCoffeeCount_1)+','+str(self._dailyCoffeeCount_2)

                coffeeJson = {'daily': self._dailyCoffeeCount,
                              'hourly': self._objHr,
                              'id': '2',
                              'timestamp': timestamp,
                              'total': self._totalCoffeeCount
                              }

                result = self.__firebase.post('/coffee', coffeeJson)
                if DEBUG:
                    print result

            if 2.5 < sensorVal_2 < 5:
                self._cupPresent_2 = True
                self._timer_2 += 1
            else:
                self._cupPresent_2 = False
                self._timer_2 = 0

            # self._lcd.setCursor(0, 1)
            # if DEBUG:
            #     self._lcd.message('{:.3f} Count {:d}\n'.format(sensorVal, self._dailyCoffeeCount))
            # else:
            #     self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount))

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
