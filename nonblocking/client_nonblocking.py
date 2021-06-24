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
import queue
import sys

EV_ABS = 3

inputs = []
outputs = []
send_queue = queue.Queue()
receive_queue = queue.Queue()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	print("Connecting to server...")
	client.connect(('localhost' if len(sys.argv) == 1 else sys.argv[1], 33333))
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client.setblocking(False)
	inputs.append(client)
	outputs.append(client)
	print("Connected.")	
	
	with open('/dev/input/event0', 'rb+', buffering=0) as digitizer:
		inputs.append(digitizer)
		
		while True:
			ready_to_read, ready_to_write, in_error = \
					   select.select(
						  inputs, #socket to read from
						  outputs,
						  [],
						  60)
			for obj in ready_to_read:
				#we are receiving some data from the remote client
				if obj is client:
					received_strokes = client.recv(16)
					if not len(received_strokes):
						print("Connection closed by the server.")
						sys.exit()

				#we can read from our pen and add it to the send buffer
				elif obj is digitizer:
					local_pen_data = digitizer.read(16)
					send_queue.put(local_pen_data)

			for obj in ready_to_write:
				#we can send data to remote client
				if obj is client:
					while not send_queue.empty():
						pen_data = send_queue.get_nowait()
						client.send(pen_data)
						
				#we can write data to the digitizer
				elif obj is digitizer:
					while not receive_queue.empty():
						remote_pen_data = send_queue.get_nowait()
						digitizer.write(remote_pen_data)
					
			for obj in in_error:
				print(f"Error status with {obj}")

