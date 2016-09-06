from ..synthesizer import Program

class FileType:

    extension = None

    def decode(self, data):
        program = None
        return program

    def encode(self, program):
        data = None
        return data

    def read(self, f):
        #print("* Reading: \"{}\"".format(f))
        with open(f, "rb") as infile:
            return self.decode(infile.read())

    def write(self, f, program):
        with open(f, "wb") as outfile:
            outfile.write(self.encode(program))

from .base import Base
from .text import Text
from .sysex import SysEx
from .prg import Prg

