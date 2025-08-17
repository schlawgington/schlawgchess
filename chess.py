from constants import *
from move import *

BOARD = [[EMPTY for i in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

def initboard():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if row == 0:
                BOARD[row][col] = back_rank[col]
            elif row == 7:
                BOARD[row][col] = back_rank[col].lower()
            if row == 1:
               BOARD[row][col] = ' P '
            elif row == 6:
               BOARD[row][col] = ' p '

def printboard():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                print(f"{WHITE_BACK}{BOARD[row][col]}{ESCAPE_COLOR_HELL}", end = '')
            elif (row % 2 != 0 and col % 2 == 0) or (row % 2 == 0 and col % 2 != 0):
                print(f"{BLACK_BACK}{BOARD[row][col]}{ESCAPE_COLOR_HELL}", end = '')
        print(f' {BOARD_HEIGHT - row}')
    for char in Files:
        print(f" {char} ", end = '')
    print('')

def get_pieces(player):
    pieces = {"white": {}, "black": {}}

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if BOARD[row][col].isupper():
                piece_pos_string = f"{Files[col]}{BOARD_HEIGHT - row}"
                if piece_pos_string not in pieces["black"]:
                    pieces["black"][piece_pos_string] = BOARD[row][col].strip()
            elif BOARD[row][col].islower():
                piece_pos_string = f"{Files[col]}{BOARD_HEIGHT - row}"
                if piece_pos_string not in pieces["white"]:
                    pieces["white"][piece_pos_string] = BOARD[row][col].strip()
    
    print(pieces[player])

    return pieces

def in_check(opposite_player_moves:list, player_pieces, player):
    for piece in player_pieces[player].keys():
        if player_pieces[player][piece].upper() == 'K':
            king_pos = piece
    
    check = False

    for mv in opposite_player_moves:
        if mv == king_pos:
            check = True

    player_moves = {}

    if check == True:
        for piece in player_pieces[player].keys():
            if piece not in player_moves:
                player_moves[piece] = legal_check(move(player_pieces, player, piece, BOARD), player, opposite_player_moves)

def get_in(color:str, pieces):
    user_in = input("Enter rank and file: ").upper()
    while user_in not in pieces:
        user_in = input("Enter valid rank and file: ").upper()

    return user_in

def translate(move_in:str):
    row_num = BOARD_HEIGHT - int(move_in[1])
    col_num = Filetonum[move_in[0]]

    return row_num, col_num

def game_loop(player, opposite_player):
    printboard()

    cur_pieces = get_pieces(player)

    opposite_player_moves = []
    for piece in cur_pieces[opposite_player].keys():
        opposite_player_moves.extend(move(cur_pieces, opposite_player, piece, BOARD))

    in_check(opposite_player_moves, cur_pieces, player)

    user_in = get_in(player, cur_pieces[player])
    translated_in = translate(user_in)

    legal_moves = legal_check(move(cur_pieces, player, user_in, BOARD), player, opposite_player_moves)

    untrans_move = get_in(player, legal_moves)
    
    if untrans_move == "QUEENSIDE CASTLE":
        if player == "white":
            BOARD[7][2] = BOARD[7][4]  
            BOARD[7][4] = EMPTY
            BOARD[7][3] = BOARD[7][0]  
            BOARD[7][0] = EMPTY
        elif player == "black":
            BOARD[0][2] = BOARD[0][4]  
            BOARD[0][4] = EMPTY
            BOARD[0][3] = BOARD[0][0]
            BOARD[0][0] = EMPTY
    elif untrans_move == "KINGSIDE CASTLE":
        if player == "white":
            BOARD[7][6] = BOARD[7][4]
            BOARD[7][4] = EMPTY
            BOARD[7][5] = BOARD[7][7]
            BOARD[7][7] = EMPTY
        elif player == "black":
            BOARD[0][6] = BOARD[0][4]  
            BOARD[0][4] = EMPTY
            BOARD[0][5] = BOARD[0][7] 
            BOARD[0][7] = EMPTY
    else:
        if user_in in Castle_flags[player]:
            Castle_flags[player][user_in] = False

        move_in = translate(untrans_move)
        BOARD[move_in[0]][move_in[1]] = BOARD[translated_in[0]][translated_in[1]]
        BOARD[translated_in[0]][translated_in[1]] = EMPTY

initboard()

while game:
    game_loop(player, opposite_player)
    
    player = "black" if player == "white" else "white"
    opposite_player = "black" if player == "white" else "white"