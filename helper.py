from constants import *

def initboard():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if row == 0:
                BOARD[row][col] = back_rank[col].lower()
            elif row == 7:
                BOARD[row][col] = back_rank[col]
            if row == 1:
               BOARD[row][col] = ' p '
            elif row == 6:
               BOARD[row][col] = ' P '

def printboard(BOARD_STATE):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                print(f"{WHITE_BACK}{BOARD_STATE[row][col]}{ESCAPE_COLOR_HELL}", end = '')
            elif (row % 2 != 0 and col % 2 == 0) or (row % 2 == 0 and col % 2 != 0):
                print(f"{BLACK_BACK}{BOARD_STATE[row][col]}{ESCAPE_COLOR_HELL}", end = '')
        print(f' {BOARD_HEIGHT - row}')
    for char in Files:
        print(f" {char} ", end = '')
    print('')

def get_pieces(BOARD_STATE):
    pieces = {"white": {}, "black": {}}

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if BOARD_STATE[row][col].islower():
                piece_pos_string = f"{Files[col]}{BOARD_HEIGHT - row}"
                if piece_pos_string not in pieces["black"]:
                    pieces["black"][piece_pos_string] = BOARD_STATE[row][col].strip()
            elif BOARD_STATE[row][col].isupper():
                piece_pos_string = f"{Files[col]}{BOARD_HEIGHT - row}"
                if piece_pos_string not in pieces["white"]:
                    pieces["white"][piece_pos_string] = BOARD_STATE[row][col].strip()

    return pieces #returns dict pieces {'white': {white pieces}, 'black': {black pieces}}

def in_check(opposite_player_moves:list, player_pieces, player):
    for piece in player_pieces[player].keys():
        if player_pieces[player][piece].upper() == 'K':
            king_pos = piece
    
    check = False

    for mv in opposite_player_moves:
        if mv == king_pos:
            check = True

    return check

class BackException(Exception):
    pass

#User input
def get_in(pieces, player=None):
    print(pieces)
    untranslated_piece_to_move = input("Enter rank and file: ")

    if untranslated_piece_to_move.upper() == "BACK":
        raise BackException()

    while untranslated_piece_to_move not in pieces:
        untranslated_piece_to_move = input("Enter valid rank and file: ")

        if untranslated_piece_to_move.upper() == "BACK":
            raise BackException()

    return untranslated_piece_to_move

#Translate user input to board position
def translate(translated_piece_move:str):
    row_num = BOARD_HEIGHT - int(translated_piece_move[1])
    col_num = Filetonum[translated_piece_move[0]]

    return row_num, col_num

def FEN_str_gen(BOARD, player, legal_moves, opposite_player_moves, en_passant, half_move_clock, full_move_clock):
    str_arr = []
    for row in range(BOARD_HEIGHT):
        count = 0
        for col in range(BOARD_WIDTH):
            if BOARD[row][col] == EMPTY:
                count += 1
            elif count != 0:
                str_arr.append(str(count))
                count = 0
            str_arr.append(BOARD[row][col].strip())
        if count != 0:
            str_arr.append(str(count))
        if row != 7:
            str_arr.append('/')

    if player == 'white':
        turn = 'b'
    else:
        turn = 'w'

    all_moves = [move for moves in legal_moves.values() for move in moves]

    if player == 'white':
        WK_castle_flag = 'K' if "kingside castle" in all_moves else ''
        WQ_castle_flag = 'Q' if "queenside castle" in all_moves else ''

        BK_castle_flag = 'k' if "kingside castle" in opposite_player_moves else ''
        BQ_castle_flag = 'q' if "queenside castle" in opposite_player_moves else ''

    if player == 'black':
        WK_castle_flag = 'K' if "kingside castle" in opposite_player_moves else ''
        WQ_castle_flag = 'Q' if "queenside castle" in opposite_player_moves else ''

        BK_castle_flag = 'k' if "kingside castle" in all_moves else ''
        BQ_castle_flag = 'q' if "queenside castle" in all_moves else ''

    if WK_castle_flag == '' and WQ_castle_flag == '' and BK_castle_flag == '' and BQ_castle_flag == '':
        WK_castle_flag = '-'

    FEN_str = f"{"".join(str_arr)} {turn} {WK_castle_flag}{WQ_castle_flag}{BK_castle_flag}{BQ_castle_flag} {en_passant} {half_move_clock} {full_move_clock}"

    return FEN_str

def en_passant_check(piece_type, piece_init_location, piece_final_location, player):
    pawn_validity = False
    if piece_type.strip() == 'p' or piece_type.strip() == 'P':
        pawn_validity = True

    if pawn_validity:
        if player == 'white':
            if piece_final_location[0] == piece_init_location[0] and piece_final_location[1] == '4' and piece_init_location[1] == '2':
                return f"{piece_final_location[0]}3"
        else:
            if piece_final_location[0] == piece_init_location[0] and piece_final_location[1] == '5' and piece_init_location[1] == '7':
                return f"{piece_final_location[0]}6"

    return '-'

def half_move_clock_check(piece_type, capture_flag):
    if piece_type.strip() == 'p' or piece_type.strip() == 'P' or capture_flag == True:
        return True
    else:
        return False

def FEN_str_to_BOARD(FEN_str):
    split_FEN_str = FEN_str.split("/")
    split_FEN_str_arr = []

    for split in split_FEN_str:
        row = []
        for ch in split:
            if ch.isdigit():
                row.extend([EMPTY] * int(ch))
            else:
                row.append(f" {ch} ")
        split_FEN_str_arr.append(row)

    return split_FEN_str_arr