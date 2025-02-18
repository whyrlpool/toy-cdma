#!/usr/bin/python3

import hashlib
import time
from PIL import BmpImagePlugin
import numpy

fifo_pretendserial="test.bin"

def current_time():
	return int(time.time()*1000)

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

listimage=[]
i=0
with open(fifo_pretendserial, mode="rb") as f:
	chunk = f.read(64)
	for i in range(0,64):
		xordata = [ (a ^ b) for (a,b) in zip(callsign_digest, get_timestamp_hash(i)) ]
		encoded = [ (a ^ b) for (a,b) in zip(ISHFTC(chunk,i%64), xordata) ]
		#print(bytearray(chunk), i)
		print(ISHFTC(bytearray(chunk),i%64))
		listimage.append((encoded))

#print(listimage)
flat_list= [item for sublist in listimage for item in sublist]
#print(flat_list)
#print(bytearray(flat_list))
print(len(bytearray(flat_list)))
#print(bin(int.from_bytes(bytes(flat_list), byteorder="big")))
input_image = BmpImagePlugin.BmpImageFile("blank.bmp")
output_image=input_image.copy()
output_image.frombytes(bytes(flat_list))
output_image.save('result.bmp')
