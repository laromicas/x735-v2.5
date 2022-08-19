#!/usr/bin/python3
# this python code is base python 2, not python 3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys

TACH = 16
PULSE = 2
WAIT_TIME = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = time.time()
rpm = 0

def fell(n):
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.005: return

    freq = 1 / dt
    rpm = (freq / PULSE) * 60
    t = time.time()

GPIO.add_event_detect(TACH, GPIO.FALLING, fell)

try:
    time.sleep(0.1)
    print("%.f" % rpm)
except KeyboardInterrupt:
    GPIO.cleanup()

