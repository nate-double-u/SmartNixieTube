__author__ = 'Nathan Waddington'
__email__ = 'nathan.waddington@akqa.com'
__copyright__ = 'Copyright 2014 AKQA inc. All Rights Reserved'

#!/usr/bin/python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "time.nist.gov"
port = 13
s.connect((host,port))
while True:
    data = s.recv(10000)
    if data:
        print data
        print type(data)
    else:
        break

s.close()
