def program_code_to_index(code):
    side = code[0]
    bank, program = map(int, code[1:])
    index = ((0 if side == "A" else 1) << 6) + \
            ((bank - 1) << 3) + \
            (program - 1)
    return index

def program_index_to_code(index):
    side = "A" if index >> 6 == 0 else "B"
    bank = 1 + ((index >> 3) & 7)
    program = 1 + (index & 7)
    code = "{}{}{}".format(side, bank, program)
    return code

def program_iter():
    for side in ["A", "B"]:
        for bank in range(1, 9):
            for program in range(1, 9):
                code = "{}{}{}".format(side, bank, program)
                yield code

def program_print_all():
    for i, code_iter in enumerate(program_iter()):
        code = program_index_to_code(i)
        index = program_code_to_index(code)
        assert code_iter == code
        assert i == index
        print("{:03}, {}".format(index, code))


if __name__ == "__main__":

    program_print_all()

