import difflib

with open("dumps/init_prog.prg", "rb") as infile:
    init_prog = infile.read()

with open("dumps/original-programs.syx", "rb") as infile:
    programs = infile.read()

with open("dumps/original-p_a11.syx", "rb") as infile:
    p_a11 = infile.read()


#d = difflib.SequenceMatcher(None, init_prog[25:], p_a11)
d = difflib.SequenceMatcher(None, programs, p_a11)

print(d.get_matching_blocks())

