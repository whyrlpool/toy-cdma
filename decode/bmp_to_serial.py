#!/usr/bin/python3

import hashlib
import time
from PIL import BmpImagePlugin
import numpy
from operator import add

fifo_pretendserial="test.bin"

def current_time():
	#return int(time.time()*1000)
	return int(0)

callsign = hashlib.sha512()
callsign.update(b"M6JXU")
callsign_digest=callsign.digest()

def get_timestamp_hash(N):
	timestamp = hashlib.sha512()
	timestamp.update((current_time()+N).to_bytes(32))
	return(timestamp.digest())

def ISHFTC(raw_bits, shift_amt):
	if ((shift_amt%len(raw_bits)) == 0):
		return raw_bits
	return  raw_bits[(len(raw_bits)-(shift_amt)):] + raw_bits[:-(shift_amt)]

#print(flat_list[4096*12:4096*13])
#print(flat_list)
#print(bytearray(flat_list))
#print((bytes(flat_list)))
#print(bin(int.from_bytes(bytes(flat_list), byteorder="big")))
flat_list = BmpImagePlugin.BmpImageFile("result.bmp").tobytes()
print (type(flat_list))
print (len(flat_list))

i=0
j=0
chunk = flat_list
j+=1
output_data=[0]*64
for i in range(0,12):
	chunk=flat_list[64*i:64*(i+1)]
	chunk=ISHFTC(chunk,64-((4*i)%64))
	xordata = [ (a ^ b) for (a,b) in zip(callsign_digest, get_timestamp_hash(i)) ]
	print(xordata)
	encoded = [ (a ^ b) for (a,b) in zip(chunk, xordata) ]
	#print(bytearray(chunk), i)
	#print(ISHFTC(bytearray(chunk),i%64))
	#x=(([255]*4)+([0]*64)+([255]*60))
	print(bytes(encoded))
#output_data=list(a+b for a,b in zip (encoded, output_data))
#print(bytes(output_data))
