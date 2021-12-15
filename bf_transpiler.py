import sys


translation = {
    "<": "Nya",
    ">": "nyA",
    "+": "nya",
    "-": "nYa",
    "[": "NYa",
    "]": "nYA",
    ".": "NyA",
    ",": "NYA"
}

if __name__ == '__main__':
    s = ""
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            for char in line:
                if char in translation.keys():
                    s += translation[char] + "\n"

    print(s)
