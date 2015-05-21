__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

import sys

#  $[DIGIT],[LEFT DECIMAL POINT],[RIGHT DECIMAL POINT],[BRIGHTNESS],[RED],[GREEN],[BLUE]!

class SmartNixieTubeDisplay(Exception):
    def __init__ (self, numberOfTubesInDisplay):
        if numberOfTubesInDisplay < 1:
            raise AssertionError('Must have one or more tubes.')

        self.numberOfTubesInDisplay = numberOfTubesInDisplay
