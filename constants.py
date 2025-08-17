BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT

EMPTY = '   '
Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
back_rank = [' R ', ' N ', ' B ', ' Q ', ' K ', ' B ', ' N ', ' R ']
test_back_rank = [' R ', EMPTY, EMPTY, ' Q ', ' K ', EMPTY, EMPTY, ' R ']

white = "white"
black = "black"

Filetonum = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7
    }

Castle_flags = {
    "white": {
        "A1": True,
        "E1": True,
        "H1": True
    },
    "black": {
        "A8": True,
        "E8": True,
        "H8": True
    }
}

game = True
player = "white"
opposite_player = "black"

ESCAPE_COLOR_HELL = "\033[0m"
BLACK_BACK = "\033[48;5;232m"
WHITE_BACK = "\033[48;5;15m"