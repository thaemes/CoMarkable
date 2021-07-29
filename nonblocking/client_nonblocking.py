#!/usr/bin/env python3
'''

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


just_received = False

written_data = 0

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
					print("recieved client")
					received_strokes = client.recv(16)
					if not len(received_strokes):
						print("Connection closed by the server.")
						sys.exit()					
					try:
						digitizer.write(received_strokes)
					except OSError:
						pass
					written_data += 1 
					#just_received = True


				elif obj is digitizer:
					local_pen_data = digitizer.read(16)
					if written_data > 0:
						print("continued because i just received....")
						written_data -= 1
					else:
						send_queue.put(local_pen_data)

			#we can read from our pen and add it to the send buffer
#				elif obj is digitizer:

			for obj in ready_to_write:
				#we can send data to remote client
				if obj is client:
					if not send_queue.empty():
						pen_data = send_queue.get_nowait()
						client.send(pen_data)
						
			for obj in in_error:
				print(f"Error status with {obj}")

