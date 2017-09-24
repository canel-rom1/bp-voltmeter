#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
    Project: bp-voltmeter
    File: bp-voltmeter.py
    Version: 0.1
    Create by: Rom1 <rom1@canel.ch>
               CANEL - https://www.canel.ch
    Date: 23/09/17
    License: GNU GENERAL PUBLIC LICENSE v3
    Language: Python 3
    Description: A voltmeter for the Bus Pirate in the terminal mode.

"""

import argparse
import os
import serial
import signal
import sys
from time import sleep

numbers = {
    '1': [[' $$  '],
          ['  $  '],
          ['  $  '],
          ['  $  '],
          [' $$$ ']],

    '2': [['$$$$ '],
          ['    $'],
          [' $$$ '],
          ['$    '],
          ['$$$$$']],

    '3': [['$$$$ '],
          ['    $'],
          ['  $$$'],
          ['    $'],
          ['$$$$$']],

    '4': [['  $$ '],
          ['  $$ '],
          [' $ $ '],
          ['$$$$$'],
          ['   $ ']],

    '5': [['$$$$$'],
          ['$    '],
          ['$$$$ '],
          ['    $'],
          ['$$$$ ']],

    '6': [[' $$$$'],
          ['$    '],
          ['$$$$ '],
          ['$   $'],
          [' $$$ ']],

    '7': [['$$$$$'],
          ['   $ '],
          ['  $  '],
          [' $   '],
          ['$    ']],

    '8': [[' $$$ '],
          ['$   $'],
          [' $$$ '],
          ['$   $'],
          [' $$$ ']],

    '9': [[' $$$ '],
          ['$   $'],
          [' $$$$'],
          ['    $'],
          ['$$$$ ']],

    '0': [[' $$$ '],
          ['$  $$'],
          ['$ $ $'],
          ['$$  $'],
          [' $$$ ']],

    '.': [['   '],
          ['   '],
          ['   '],
          ['$$$'],
          ['$$$']],

    'V': [['$   $'],
          ['$   $'],
          ['$   $'],
          [' $ $ '],
          ['  $  ']],
}

arguments = argparse.ArgumentParser()
arguments.add_argument("-b", "--big", action="store_true", help="Big chars")
arguments.add_argument("-d", "--device", type=str, default="/dev/buspirate0", help="Serial port device")
arguments.add_argument("-s", "--speed", type=int, default=115200, help="Serial port baud rate")
args = arguments.parse_args()

bp = serial.Serial(args.device, args.speed, timeout = 0.1)

def quit(signal, frame):
    bp.write(b'\x0F')
    sleep(0.1)
    bp.reset_input_buffer()
    sleep(0.1)
    bp.close()
    sys.exit(0)
signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

def printValue(value):
    for l in range(0,5):
        for n in range(0,5):
            print(str(numbers[value[n]][l][0]), end='  ')
        print()

bp.write(b'\n')
sleep(0.1)

x = 0
while True and x < 10:
    x += 1
    data_recv = bp.read(6)
    if data_recv == b'':
        break
bp.reset_input_buffer()
sleep(0.1)

while True:
    bp.write(b'd\n')
    bp.reset_input_buffer()
    x = 0
    while True and x < 10:
        x += 1
        data_recv = bp.read(3)
        if data_recv == b'd\r\n':
            break
    voltage = str(bp.read(20))
    x = 0
    while True and x < 10:
        x += 1
        data_recv = bp.read(2)
        if data_recv == b'\r\n':
            break
    sleep(0.1)
    os.system("clear")
    print("BUS PIRATE")
    print("Voltage (Adc: 4 ; GND: 1):")
    if args.big:
        printValue(voltage[17:-1])
    else:
        print(voltage[17:-1])
    print("CTRL + C for Quit")


# vim: ft=python ts=8 et sw=4 sts=4
