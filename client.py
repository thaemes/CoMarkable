#!/usr/bin/env python3
'''
Based on LinusCDE's rmWacomToMouse
https://github.com/LinusCDE/rmWacomToMouse 
'''

from sys import argv
import os
import socket
import struct

# ----------


ONLY_DEBUG=False  # Only show data. Don't move mouse

WACOM_WIDTH = 15725   # Values just checked by drawing to the edges
WACOM_HEIGHT = 20967  # ↑

screenRectWidth = SCREEN_DRAW_AREA_TO_X - SCREEN_DRAW_AREA_FROM_X
screenRectHeight = SCREEN_DRAW_AREA_TO_Y - SCREEN_DRAW_AREA_FROM_Y
ratioX = screenRectWidth / WACOM_WIDTH
#ratioY = screenRectHeight / WACOM_HEIGHT
ratioY = ratioX

# Source: https://github.com/canselcik/libremarkable/blob/master/src/input/wacom.rs
EV_SYNC = 0
EV_KEY = 1
EV_ABS = 3
WACOM_EVCODE_PRESSURE = 24
WACOM_EVCODE_DISTANCE = 25
WACOM_EVCODE_XTILT = 26
WACOM_EVCODE_YTILT = 27
WACOM_EVCODE_XPOS = 0
WACOM_EVCODE_YPOS = 1

lastXPos = -1
lastYPos = -1
lastXTilt = -1
lastYTilt = -1
lastDistance = -1
lastPressure = -1


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0' if len(argv) == 1 else argv[1], 33333))

# Source: https://github.com/DAA233/kalman-filter/

wacomEvents = os.open('/dev/input/event0', os.O_WRONLY)

try:
        while True:
                rec = client.recv(16)
                tmp, evDevType, evDevCode, evDevValue = struct.unpack('QHHi', rec)	
                os.write(wacomEvents, rec)
                if evDevType == EV_ABS:
                        if evDevCode == WACOM_EVCODE_XPOS:
                                lastYPos = evDevValue  # X is Y
                        elif evDevCode == WACOM_EVCODE_YPOS:
                                lastXPos = evDevValue  # Y is X
                        elif evDevCode == WACOM_EVCODE_XTILT:
                                lastXTilt = evDevValue
                        elif evDevCode == WACOM_EVCODE_YTILT:
                                lastYTilt = evDevValue
                        elif evDevCode == WACOM_EVCODE_DISTANCE:
                                lastDistance = evDevValue
                        elif evDevCode == WACOM_EVCODE_PRESSURE:
                                lastPressure = evDevValue
                print('XPos: %5d | YPos: %5d | XTilt: %5d | YTilt: %5d | Distance: %3d | Pressure: %4d' % (lastXPos, lastYPos, lastXTilt, lastYTilt, lastDistance, lastPressure))

finally:
        os.close(wacomEvents)

