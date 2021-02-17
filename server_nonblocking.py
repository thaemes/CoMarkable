#!/usr/bin/env python3
'''
Based on LinusCDE's rmWacomToMouse
https://github.com/LinusCDE/rmWacomToMouse 
Meant to run on the reMarkable.
Opens a server on 10.11.99.1:33333 (or any wifi ip)
and sends all event data to the next client.
'''

import socket
import struct
import select
import pdb

EV_ABS = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 33333))
server.listen()
server.setblocking(False)

wacomEvents = ''

try:
	while True:
		print('Waiting for client...')
		ready_to_read, ready_to_write, in_error = \
				   select.select(
					  [server], #socket to read from
					  [],
					  [],
					  60)
		if server in ready_to_read:
			client, addr = server.accept()
			print('Client connected')
			# Start reading input from wacom digitizer:
			wacomEvents = open('/dev/input/event0', 'rb')
	
			while True:
				#check whether we can read data from pen and/or socket
				ready_to_read, ready_to_write, in_error = \
				   select.select(
					  [wacomEvents,server], #socket to read from (tablet & client
					  [server],
					  [],
					  60)
				#if we have data from the pen, read it
				if wacomEvents in ready_to_read:
					local_pen_data = wacomEvents.read(16)
					
					#doesn't work yet, BUT might be because the client is in blocking mode?
					#if server in ready_to_write:
					client.send(local_pen_data) 
finally:
	wacomEvents.close()
	server.close()
