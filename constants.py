import copy
import math
import random

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT
EMPTY = '   '

BOARD = [[EMPTY for i in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

Files = ["a", "b", "c", "d", "e", "f", "g", "h"]
back_rank = [' R ', ' N ', ' B ', ' Q ', ' K ', ' B ', ' N ', ' R ']
test_back_rank = [' R ', EMPTY, EMPTY, ' Q ', ' K ', EMPTY, EMPTY, ' R ']

Filetonum = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

Castle_flags = {
    "white": {
        "a1": True,
        "e1": True,
        "h1": True
    },
    "black": {
        "a8": True,
        "e8": True,
        "h8": True
    }
}

Material_dict = {
    'K': 200,
    'Q': 9,
    'R': 5,
    'N': 3,
    'B': 3,
    'P': 1
}

ESCAPE_COLOR_HELL = "\033[0m"
BLACK_BACK = "\033[48;5;232m"
WHITE_BACK = "\033[48;5;15m"