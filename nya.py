import sys
from typing import List, Callable, Tuple

from ops import prev, next, incr, decr, jmpt, jmpf, sout, sinp, generate_braces

braces: dict[int, int] = {}

OP_CODES: dict[str, [Callable[[List[int], int], int], Tuple[int, int]]] = {
    "Nya": prev,  # < prev
    "nyA": next,  # > next
    "nya": incr,  # + incr
    "nYa": decr,  # - decr
    "NYa": jmpt,  # [ jmpt
    "nYA": jmpf,  # ] jmpf
    "NyA": sout,  # . sout
    "NYA": sinp,  # , sinp
}





def run(filename: str):
    with open(filename) as f:
        instructions = [line.rstrip() for line in f.readlines()]
    generate_braces(instructions)
    instr_ptr = 0
    data = [0]
    data_ptr = 0
    while instr_ptr < len(instructions):
        op = OP_CODES[instructions[instr_ptr]]
        data_ptr, instr_ptr = op(data, data_ptr, instr_ptr)
        instr_ptr += 1


if __name__ == '__main__':
    # todo: use pattern matching here
    if len(sys.argv) != 2:
        print(f"You fucked up. Run your catgirls properly baka.")
    else:
        run(sys.argv[1])
