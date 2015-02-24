#!/usr/bin/env python2.7
# This script should automatically detect your 1-wire sensors
# It will load device drivers for them if needed
# Just wire them up and run it
# By Alex Eames http://RasPi.TV
import subprocess
import os
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(24, GPIO.OUT) # 24 for led
GPIO.setup(23, GPIO.OUT) # 23 for LDR light sensor

try:
    w1_devices = os.listdir("/sys/bus/w1/devices/")
except:
    print "Loading 1-wire device drivers, please wait five seconds..."
    output_mp1 = subprocess.Popen('sudo modprobe w1-gpio', shell=True, stdout=subprocess.PIPE)
    output_mp2 = subprocess.Popen('sudo modprobe w1-therm', shell=True, stdout=subprocess.PIPE)
    time.sleep(5)        # wait a few seconds to stop the program storming ahead and crashing out
#    print "failed first time"
    w1_devices = os.listdir("/sys/bus/w1/devices/")

#print w1_devices
no_of_devices = len(w1_devices) -1
print "You have %d 1-wire devices attached" % (no_of_devices)

if no_of_devices < 1:
    print "Please check your wiring and try again."
    sys.exit()

w1_device_list = []

for device in w1_devices:
    if not ('w1_bus' in device):
#        print device
        # create string for calling each device and append to list
        this_device = "/sys/bus/w1/devices/" + device + "/w1_slave"
#        print this_device
        w1_device_list.append(this_device)

#print w1_device_list

def read_temp(device):
    DS18b20 = open(device)
    text = DS18b20.read()
    DS18b20.close()

    # Split the text with new lines (\n) and select the second line.
    secondline = text.split("\n")[1]

    # Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
    temperaturedata = secondline.split(" ")[9]

    # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
    temperature = float(temperaturedata[2:])

    # Put the decimal point in the right place and display it.
    temperature = temperature / 1000
    return temperature


def msr_time(msr_pin):
    reading = 0
    GPIO.setup(msr_pin, GPIO.OUT)
    GPIO.output(msr_pin, GPIO.LOW)
    time.sleep(0.1)
    starttime = time.time()                     # note start time
    GPIO.setup(msr_pin, GPIO.IN)
    while (GPIO.input(msr_pin) == GPIO.LOW):
        reading += 1
    endtime = time.time()                       # note end time
    total_time = 1000 * (endtime - starttime)
    return total_time                           # reading in milliseconds

reps = 20
while True:
    if reps % 20 == 0:
        print "\nHit CTRL+C to exit the program, when you're done\n"
    sensor = 1
    for device in w1_device_list:
        temperature = read_temp(device)
        if sensor == 1:
            if temperature > 25:
                GPIO.output(24, 1)
            else:
                GPIO.output(24, 0)
        print "sensor %d: %.2f C" % (sensor, temperature)
        sensor += 1
    time.sleep(1)
    reps += 1
    print "light level: %.3f" % (1 / msr_time(23) / 6.0)

# need to add try except to clean up GPIO now we're using it

