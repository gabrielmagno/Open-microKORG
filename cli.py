#!/usr/bin/env python3

import sys
import bitstring

import microkorg

if __name__ == "__main__":

    filename = sys.argv[1]

    if filename[-3:] == "prg":
        programs = microkorg.filetypes.Prg().read(filename)
    elif filename[-3:] == "syx": 
        programs = microkorg.filetypes.SysEx().read(filename)

    for program in programs:
        #print(program.name)
        print(microkorg.filetypes.Text().encode(program))

