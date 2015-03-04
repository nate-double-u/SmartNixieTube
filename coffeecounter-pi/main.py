__author__ = 'Nathan Waddington & Mark Liang'
__copyright__ = 'Copyright 2015 AKQA inc. All Rights Reserved'

import sys

from coffeecounter import CoffeeCounter
import RPi.GPIO as GPIO


def main():
    """main"""

    coffeeMachine1 = CoffeeCounter()
    coffeeMachine2 = CoffeeCounter()

    # main loop
    while True:
        coffeeMachine1.count()
        coffeeMachine2.count()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt.")
        GPIO.cleanup()
