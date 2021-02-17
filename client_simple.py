#!/usr/bin/env python3
'''
Based on LinusCDE's rmWacomToMouse
https://github.com/LinusCDE/rmWacomToMouse 
'''

from sys import argv
import os
import socket
import struct


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('143.178.219.194' if len(argv) == 1 else argv[1], 33333))


wacomEvents = open('/dev/input/event0', "rb+", buffering=0)

rec = ""

try:
	while True:
		rec = client.recv(16)
		if len(rec) == 16:
			wacomEvents.write(rec)
	
finally:
	print(rec)
	wacomEvents.close()

