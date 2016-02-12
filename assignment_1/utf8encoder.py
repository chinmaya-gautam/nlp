#!/usr/bin/python

import sys
import struct

input_path = sys.argv[1]

file = open(input_path, "rb")
outfile = open("utf8encoder_out.txt", "wb")

while True:
    data = file.read(2)
    if not data:
        break
    bytes = struct.unpack('>h',data)[0]
    if bytes <= int('0x7f', 16):
        #case1
        octet1 = int('0b01111111', 2) & bytes
        #print hex(octet1)
        output = struct.pack('c', chr(octet1))
        outfile.write(output)
    elif bytes <= int('0x7ff', 16):
        #case2
        octet1 = int('0b00111111', 2) & bytes
        octet1 = octet1 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet2 = int('0b00011111', 2) & bytes
        octet2 = octet2 | int('0b11000000', 2)
        output = struct.pack('c', chr(octet2))
        outfile.write(output)
        output = struct.pack('c', chr(octet1))
        outfile.write(output)
        #print hex(octet2), hex(octet1)
    elif bytes <= int('0xffff', 16):
        #case3
        octet1 = int('0b00111111', 2) & bytes
        octet1 = octet1 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet2 = int('0b00111111', 2) & bytes
        octet2 = octet2 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet3 = int('0b00001111', 2) & bytes
        octet3 = octet3 | int('0b11100000', 2)
        output = struct.pack('c', chr(octet3))
        outfile.write(output)
        output = struct.pack('c', chr(octet2))
        outfile.write(output)
        output = struct.pack('c', chr(octet1))
        outfile.write(output)
    elif bytes <= int('0x10ffff', 16):
        #case4
        octet1 = int('0b00111111', 2) & bytes
        octet1 = octet1 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet2 = int('0b00111111', 2) & bytes
        octet2 = octet2 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet3 = int('0b00111111', 2) & bytes
        octet3 = octet3 | int('0b10000000', 2)
        bytes = bytes >> 6
        octet4 = int('0b00000111', 2) & bytes
        octet4 = octet4 | int('0b11110000', 2)
        output = struct.pack('c', chr(octet4))
        outfile.write(output)
        output = struct.pack('c', chr(octet3))
        outfile.write(output)
        output = struct.pack('c', chr(octet2))
        outfile.write(output)
        output = struct.pack('c', chr(octet1))
        outfile.write(output)
        #print hex(octet3), hex(octet2), hex(octet1)
    else:
        print "error converting input file!!"
        break

    #print hex(bytes), int(bytes)

file.close()
