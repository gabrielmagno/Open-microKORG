import json
import collections
import bitstring

import lookup as lkp


def decode_8to7(data_encoded):
    data = bytearray()
    for ptr in range(0, len(data_encoded), 8):
        chunk = data_encoded[ptr : (ptr + 8)]
        bit7s = chunk[0]
        for byte8 in chunk[1:]:
            byte7 = byte8 | (0x80 if (bit7s & 0x01) else 0x00)
            data.append(byte7)
            bit7s = bit7s >> 1
    return data

FORMAT_PROGRAM_PARAMETER = """
bytes:12,
pad:16, 

uint:5=0, 
uint:3, 

bits:8, 

uint:2=0, 
uint:2, 
uint:4=0,

uint:4=0,
uint:4=0,

pad:8,

uint:1,
uint:3=0,
uint:4,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:16,

uint:1,
uint:1,
uint:2,
pad:2,
uint:1=0,
uint:1,

uint:4,
uint:4,

uint:8,

uint:8,

uint:8,

uint:8,
"""

FORMAT_SYNTH_PARAMETER = """
int:8,

uint:2,
uint:1,
uint:1,
uint:1,
pad:1,
uint:2=0,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

uint:8,

pad:8,

uint:2=0,
uint:2,
uint:2=0,
uint:2,

uint:8,

uint:8,

uint:1=0,
uint:7,
"""

def unpack(data):

    bits = bitstring.ConstBitStream(data)

    print(bits.pos)
    print(bits.bytepos)
    decoded = bits.readlist(FORMAT_PROGRAM_PARAMETER)
    print(decoded)

    print(bits.pos)
    print(bits.bytepos)
    decoded = bits.readlist(FORMAT_SYNTH_PARAMETER)
    print(decoded)

    #encoded = bitstring.pack(DATA_FORMAT, **decoded)
    #print(encoded)

if __name__ == "__main__":

    import sys

    with open(sys.argv[1], "rb") as infile:
        data_raw = infile.read()
        data_encoded = data_raw[30:296]
        data = decode_8to7(data_encoded)
        unpack(data)

    #info = collect_all(data)
    #print(json.dumps(info, indent=4))
    
