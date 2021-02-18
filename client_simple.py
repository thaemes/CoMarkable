#!/usr/bin/env python3
'''
Based on LinusCDE's rmWacomToMouse
https://github.com/LinusCDE/rmWacomToMouse 
'''

from sys import argv
import os
import socket
import struct


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	client.connect(('143.178.219.194' if len(argv) == 1 else argv[1], 33333))

	with open('/dev/input/event0', "rb+", buffering=0) as wacomEvents:
		rec = ""
		try:
			while True:
				rec = client.recv(16)
				if len(rec) == 16:
					wacomEvents.write(rec)
		except Exception as e:
			print(f"Something Bad happened: {e}")
			print(f"Last received message: {rec}")
		except KeyboardInterrupt:
			print("Gracefully quitting...")
			exit()