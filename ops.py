from typing import List, Dict, Any

from getch import getch

braces: dict[int, int] = {}


def generate_braces(instructions):
    stack = []
    for idx, nya in enumerate(instructions):
        if nya == "NYa":
            stack.append(idx)
        elif nya == "nYA":
            this = stack.pop()
            braces[this] = idx
            braces[idx] = this


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
