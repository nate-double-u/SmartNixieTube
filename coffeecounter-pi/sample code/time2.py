__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

import socket
import struct
import time

from dateutil import parser


hostname = 'time.nist.gov'
port = 37

host = socket.gethostbyname(hostname)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('', (host, port))

parsedDate = parser.parse("")
print parsedDate

print "Looking for replies; press Ctrl-C to stop."
buf = s.recvfrom(2048)[0]
if len(buf) != 4:
    print "Wrong-sized reply %d: %s" % (len(buf), buf)
    sys.exit(1)

secs = struct.unpack("!I", buf)[0]
secs -= 2208988800

dateString = time.ctime(int(secs))
print dateString

parsedDate = parser.parse(dateString)
print type(parsedDate)
print parsedDate


# set the system clock
import sys
import datetime

# time_tuple = ( 2012,  # Year
#                9,  # Month
#                6,  # Day
#                0,  # Hour
#                38,  # Minute
#                0,  # Second
#                0,  # Millisecond
# )

time_tuple = ( parsedDate.year,
               parsedDate.month,
               parsedDate.day,
               parsedDate.hour,
               parsedDate.minute,
               parsedDate.second,
               0,  # millisecond
)


def _linux_set_time(time_tuple):
    import ctypes
    import ctypes.util
    import time

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    # {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple()))
    ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


if sys.platform == 'linux2':
    _linux_set_time(time_tuple)
