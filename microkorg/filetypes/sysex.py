import bitstring

from . import FileType
from .base import Base, decode_8to7
from ..synthesizer import Program

SYSEX_HEADER = "0xf0423058"
SYSEX_FOOTER = "0xf7"

SYSEX_FUNCTIONS = [
    0x10, "CURRENT PROGRAM DATA DUMP REQUEST",
    0x1C, "PROGRAM DATA DUMP REQUEST",
    0x0E, "GLOBAL DATA DUMP REQUEST",
    0x0F, "ALL DATA DUMP REQUEST",
    
    0x40, "CURRENT PROGRAM DATA DUMP",
    0x4C, "PROGRAM DATA DUMP",
    0x51, "GLOBAL DATA DUMP",
    0x50, "ALL DATA DUMP",
    
    0x11, "PROGRAM WRITE REQUEST",
]

class SysEx(FileType):
    
    def encode_message(self, func, data=None):
        s = BitArray()
        s.append(SYSEX_HEADER) 
        s.apend(func)
        if data:
            s.append(data)
        s.append(SYSEX_FOOTER) 
        return s
    
    def decode_message(self, raw):
        raw = bitstring.ConstBitStream(raw)
        header = raw.read("hex:32")
        func = raw.read("hex:8")
        _data = list(raw.split(SYSEX_FOOTER, start=40, bytealigned=True))
        if len(_data) > 1:
            data, footer = _data
        else:
            data = None
            footer = data[0]
        return header, func, data, footer

    def decode(self, raw):
        header, func, data, footer = self.decode_message(raw)
        data = decode_8to7(data.bytes)
        if func == "40":
            response = [ Base().decode(data) ]
        elif func == "4c":
            response = [ Base().decode(data) for i in range(128) ]
        else:
            print("ERROR")
            response = None
        return response

