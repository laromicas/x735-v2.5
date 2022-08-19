#!/usr/bin/python3
# this python code is base python 2, not python 3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import os

TACH = 16
PULSE = 2
WAIT_TIME = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = time.time()
rpm = 0

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def sizeof_fmt(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    return str(bytes) + units[0] if bytes < 1024 else sizeof_fmt(bytes>>10, units[1:])

def free_space(mount_point):
    st = os.statvfs(mount_point)
    freespace = st.f_bavail * st.f_frsize
    return sizeof_fmt(freespace)

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
    while True:
        # rpm = 0
        file = open("/sys/class/thermal/thermal_zone0/temp")
        temp = float(file.read()) / 1000.00
        temp = float('%.2f' % temp)
        file.close()
        time.sleep(1)
        print(f"\r{rpm:.2f} RPM   {temp:.2f}°C   mame={free_space('/mnt/mame/')}   torrents={free_space('/mnt/torrents/')}", end='')


except KeyboardInterrupt:
    GPIO.cleanup()
    print('')

