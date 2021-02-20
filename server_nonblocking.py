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

EV_ABS = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 33333))
server.listen()
server.setblocking(False)
inputs = [server]
outputs = []
send_queue = queue.Queue()
receive_queue = queue.Queue()


try:
	print('Waiting for client...')
	with open('/dev/input/event0', 'rb') as digitizer:
		inputs.append(digitizer)
		while True:

			ready_to_read, ready_to_write, in_error = \
					   select.select(
						  inputs, #socket to read from
						  outputs,
						  [],
						  60)
			for obj in ready_to_read:
				#we can connect to the client
				if obj is server:
					connection, client_address = server.accept()
					print(f'Client connected: {client_address} {connection.fileno()}')
					connection.setblocking(False)
					inputs.append(connection)
					outputs.append(connection)
				#we can read something from the client
				elif isinstance(obj,socket.socket):
					#todo: write this data we are receiving to digitizer
					print('received remote data (unhandled)')
				#we can read from our pen and add it to the send buffer
				elif obj is digitizer:
					local_pen_data = digitizer.read(16)
					send_queue.put(local_pen_data)

			for obj in ready_to_write:
				#we can send data
				if isinstance(obj,socket.socket):
					while not send_queue.empty():
						pen_data = send_queue.get_nowait()
						obj.send(pen_data)
				#we can write data to the digitizer
				elif obj is digitizer:
					while not receive_queue.empty():
						pen_data = send_queue.get_nowait()
						#write pen data to the digitizer
					
			for obj in in_error:
				print(f"Error status with {obj}")
finally:
	server.close()
