#!/usr/bin/env python3
'''
Based on LinusCDE's rmWacomToMouse
https://github.com/LinusCDE/rmWacomToMouse 
'''

from sys import argv
import os
import socket
import struct
import pdb 
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('143.178.219.194' if len(argv) == 1 else argv[1], 33333))


wacomEvents = os.open('/dev/input/event0', os.O_WRONLY)

bufferLength = 900
eventBuffer = []


try:
        while True:
                rec = client.recv(16)
                #tmp, evDevType, evDevCode, evDevValue = struct.unpack('QHHi', rec)	
                eventBuffer.append(rec)
                if len(eventBuffer) > bufferLength: # missing one os event
                        time.sleep(20)
                        for i in eventBuffer:
                                try:
                                        os.write(wacomEvents, i)
                                except:
                                        pass
                        eventBuffer = []        
                        #os.write(wacomEvents, rec)
except Exception as e:
        print(e)
        pdb.set_trace()
                                
finally:
        os.close(wacomEvents)
        
