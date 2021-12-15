import sys
from typing import List


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()

braces: dict[int, int] = {}


def next(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    data_ptr += 1
    if data_ptr == len(data):
        data.append(0)

    return data_ptr, instr_ptr


def prev(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    data_ptr -= 1
    if data_ptr < 0:
        data_ptr = 0
    return data_ptr, instr_ptr


def incr(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    data[data_ptr] += 1
    if data[data_ptr] > 255:
        data[data_ptr] = 0
    return data_ptr, instr_ptr


def decr(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    data[data_ptr] -= 1
    if data[data_ptr] < 0:
        data[data_ptr] = 255
    return data_ptr, instr_ptr


def jmpt(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    if data[data_ptr] == 0:
        return data_ptr, braces[instr_ptr]
    else:
        return data_ptr, instr_ptr


def jmpf(data: List[int], data_ptr: int, istr_ptr: int) -> (int, int):
    if data[data_ptr] != 0:
        return data_ptr, braces[istr_ptr]
    else:
        return data_ptr, istr_ptr


def sout(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    print(chr(data[data_ptr]), end="")
    return data_ptr, instr_ptr


def sinp(data: List[int], data_ptr: int, instr_ptr: int) -> (int, int):
    data[data_ptr] = ord(getch())
    return data_ptr, instr_ptr


OP_CODES = {
    "Nya": prev,  # < prev
    "nyA": next,  # > next
    "nya": incr,  # + incr
    "nYa": decr,  # - decr
    "NYa": jmpt,  # [ jmpt
    "nYA": jmpf,  # ] jmpf
    "NyA": sout,  # . sout
    "NYA": sinp,  # , sinp
}


def generate_braces(instructions):
    stack = []
    for idx, nya in enumerate(instructions):
        if nya == "NYa":
            stack.append(idx)
        elif nya == "nYA":
            this = stack.pop()
            braces[this] = idx
            braces[idx] = this


def run(filename: str):
    instructions = []
    with open(filename) as f:
        instructions = [line.rstrip() for line in f.readlines()]
    generate_braces(instructions)
    instr_ptr = 0
    data = [0]
    data_ptr = 0
    while instr_ptr < len(instructions):
        func = OP_CODES[instructions[instr_ptr]]
        data_ptr, instr_ptr = func(data, data_ptr, instr_ptr)
        instr_ptr += 1


if __name__ == '__main__':
    # todo: use pattern matching here
    if len(sys.argv) != 2:
        print(f"You fucked up. Run catgirl like: catgirl 'your_file.nya'")
    else:
        run(sys.argv[1])
