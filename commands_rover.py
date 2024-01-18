
import os
import sys
import RPi.GPIO as GPIO
import time
sys.path.append(os.path.abspath(os.path.join( '/home/pi/Documents/sphero-sdk-raspberrypi-python/')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import *

MOTOR_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_PIN, GPIO.OUT, initial=GPIO.LOW)

rvr = SpheroRvrObserver()
dir(SpheroRvrObserver)


def rover_init():
    rvr.wake()


def rover_drive_forward(speed, duration = 1.0):
    rvr.drive_tank_normalized(speed, speed)
    time.sleep(duration)
    rvr.drive_tank_normalized(0, 0)

def rover_rotator_turn(left,right):
    rvr.drive_tank_normalized(left,right)
    print("in the great function")

def rover_stop():
    rvr.drive_tank_normalized(0, 0)

def wing_motor_activate(motor_on_time):
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    time.sleep(motor_on_time)
    GPIO.output(MOTOR_PIN, GPIO.LOW)