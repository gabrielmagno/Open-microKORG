import bitstring 

from . import FileType
from .sysex import SysEx
from ..synthesizer import Program

PRG_FOOTER = "0x00ff2f00"

class Prg(FileType):

    def decode_message(self, raw):
        raw = bitstring.ConstBitStream(raw)
        header, _data = raw.split("0xf082", bytealigned=True)
        data, footer = _data.split(PRG_FOOTER, start=16, bytealigned=True) 
    
        #print("+ Header ({}) = {}".format(len(header) / 8, header))
        #print("+ _data ({}) = {}".format(len(_data) / 8, _data))
        #print("+ Data ({}) = {}".format(len(data) / 8, data))
        #print("+ OK_Data ({}) = {}".format(len(raw[200:]) / 8, raw[200:]))
        #print("+ Footer ({}) = {}".format(len(footer) / 8, footer))

        return header, data, footer

    def decode(self, raw):
        header, data, footer = self.decode_message(raw)
        program = SysEx().decode(data)
        return program

