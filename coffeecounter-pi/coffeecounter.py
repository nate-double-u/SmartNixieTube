__author__ = 'Nathan Waddington  & Mark Liang'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

# from time import sleep

import time
import datetime

from firebase import firebase

import RPi.GPIO as GPIO

# Define GPIO to use on Pi
GPIO_TRIGGER = [22, 17]
GPIO_ECHO = [27, 4]

TIMEOUT = 0

from Adafruit_CharLCD import Adafruit_CharLCD  # 1


class CoffeeCounter(object):
    _dailyCoffeeCount = [0, 0, 0]  # [total, id#1, id#2]
    _totalCoffeeCount = 0
    _objHr = {}
    _cupPresent = False
    _timer = 0
    _reset = False
    _id = 0

    _lcd = Adafruit_CharLCD() # 2

    def __init__(self, machineID):  # global
        """this is the set-up phase, get things ready!"""
        self._id = machineID

        # setup backend
        self.__firebase = firebase.FirebaseApplication('https://amber-torch-2593.firebaseio.com/', None)
        obj = self.__firebase.get('/coffee', None)

        if obj is None:
            self._totalCoffeeCount = 0
        else:
            self._totalCoffeeCount = len(obj)

        # setup GPIO stuff
        # Use BCM GPIO references instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set pins as output and input
        GPIO.setup(GPIO_TRIGGER[self._id - 1], GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_ECHO[self._id - 1], GPIO.IN)  # Echo

        # 3
        self._lcd.begin(16, 2)
        self._lcd.clear()
        self._lcd.message('AKQA JavaCounter\n')

        self._lcd.setCursor(0, 1)
        self._lcd.message('                ')

    def _getSensorValue(self, id_num):  # individual function
        # Set trigger to False (Low)
        trigger = GPIO_TRIGGER[id_num - 1]
        echo = GPIO_ECHO[id_num - 1]

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
        elapsed = stop - start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance /= 5.4
        print "Coffee Machine #" + str(id_num) + ": " + str(distance) + " inch"
        return distance

    def incrementDailyCoffeeCount(self, id_num):  # individual function
        # if self._currentDay == datetime.datetime.now().day:
        self.__firebase = firebase.FirebaseApplication('https://amber-torch-2593.firebaseio.com/', None)
        obj = self.__firebase.get('/coffee', None)
        self._totalCoffeeCount = self._totalCoffeeCount = len(obj)

        self._dailyCoffeeCount[id_num] += 1
        self._dailyCoffeeCount[0] += 1
        # else:
        #     self._dailyCoffeeCount = 1  # would be zero, but this is the first coffee of the day!
        #     self._currentDay = datetime.datetime.now().day

    def count(self):  # individual function
        # what's the sensor telling us
        sensorVal = self._getSensorValue(self._id)

        # reset every hour
        if datetime.datetime.now().minute == 0 and self._reset is False:
            for x in range(1, len(self._dailyCoffeeCount)):
                self._dailyCoffeeCount[x] = 0
            self._reset = True
        if self._reset is True:
            if datetime.datetime.now().minute == 1:
                self._reset = False

                # count the coffees! (check for the light, and increment the counter when it goes off.
        if self._cupPresent and (sensorVal > 5 or sensorVal < 2.5) and self._timer > TIMEOUT:
            self.incrementDailyCoffeeCount(self._id)

            # send the info to the backend
            timestamp = str(datetime.datetime.now())
            hr = str(datetime.datetime.now().hour)
            self._objHr[hr] = str(self._dailyCoffeeCount[1])+','+str(self._dailyCoffeeCount[2])
            coffeeJson = {'daily': self._dailyCoffeeCount[0],
                          'hourly': self._objHr,
                          'id': self._id,
                          'timestamp': timestamp,
                          'total': self._totalCoffeeCount
            }

            result = self.__firebase.post('/coffee', coffeeJson)

            self._lcd.setCursor(0, 1)
            self._lcd.message('Count {:d}\n'.format(self._dailyCoffeeCount[0]))

        if 2.5 < sensorVal < 5:
            self._cupPresent = True
            self._timer += 1
        else:
            self._cupPresent = False
            self._timer = 0

        # give the system some time before the next goround
        time.sleep(0.1)


