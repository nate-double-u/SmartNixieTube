__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

import unittest

from SmartNixieTube import SmartNixieTubeDisplay


class testSmartNixieTube(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SmartNixieTube_initialisation(self):
        numberOfTubesInDisplay = 3
        smartNixieTubeDisplay = SmartNixieTubeDisplay(numberOfTubesInDisplay)
        self.assertEqual(smartNixieTubeDisplay.numberOfTubesInDisplay, numberOfTubesInDisplay)

    def test_SmartNixieTube_initialisation_with_no_tubes(self):
        numberOfTubesInDisplay = 0

        try:
            smartNixieTubeDisplay = SmartNixieTubeDisplay(numberOfTubesInDisplay)  # this should fail
            self.fail("Didn't raise AssertionError")
        except AssertionError, e:
            self.assertEquals('Must have one or more tubes.', e.message)

    def test_SmartNixieTube_BuildNumberString(self):
        numberOfTubesInDisplay = 3
        smartNixieTubeDisplay = SmartNixieTubeDisplay(numberOfTubesInDisplay)

        self.assertEquals(smartNixieTubeDisplay.buildNumberString(0), '000')
        self.assertEquals(smartNixieTubeDisplay.buildNumberString(1), '001')
        self.assertEquals(smartNixieTubeDisplay.buildNumberString(10), '010')
        self.assertEquals(smartNixieTubeDisplay.buildNumberString(100), '100')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
