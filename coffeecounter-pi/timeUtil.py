__author__ = 'Nathan Waddington & Mark Liang'
__copyright__ = 'Copyright 2015 AKQA inc. All Rights Reserved'

import struct
import ctypes
import ctypes.util
import time

import socket
import datetime
from subprocess import *
from dateutil import parser

# Time Stuff
nistHostName = 'time.nist.gov'
nistPort = 37

nistHost = socket.gethostbyname(nistHostName)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('', (nistHost, nistPort))


class TimeUtil(object):
    _currentDay = 0

    # Time stuff
    def __init__(self):
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
        print("init time")
        # Boot info
        cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"  # get the device ip address

    def _set_system_time(self, time_tuple):  # time-stuffs
        CLOCK_REALTIME = 0

        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),  # seconds
                        ("tv_nsec", ctypes.c_long)]  # nanoseconds

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple()))
        ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

    def _getNistTime(self):  # time-stuffs
        buf = s.recvfrom(2048)[0]
        if len(buf) != 4:
            print('len(buf) != 4')
            sys.exit(1)  # TODO: Handle this exception better

        secs = struct.unpack("!I", buf)[0]
        secs -= 2208988800

        dateString = time.ctime(int(secs))
        return parser.parse(dateString)
