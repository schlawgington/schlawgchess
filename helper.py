from constants import *

#Board setup
def initboard(test_board):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if row == 0:
                test_board[row][col] = back_rank[col].lower()
            elif row == 7:
                test_board[row][col] = back_rank[col]
            if row == 1:
               test_board[row][col] = ' p '
            elif row == 6:
               test_board[row][col] = ' P '

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

def PrintBitBoard(Bitboard):
    for i in range(BOARD_HEIGHT):
        print(Bitboard[i])

#Fix later
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

    if player == 'White':
        turn = 'b'
    else:
        turn = 'w'

    all_moves = [move for moves in legal_moves.values() for move in moves]

    if player == 'White':
        WK_castle_flag = 'K' if "kingside castle" in all_moves else ''
        WQ_castle_flag = 'Q' if "queenside castle" in all_moves else ''

        BK_castle_flag = 'k' if "kingside castle" in opposite_player_moves else ''
        BQ_castle_flag = 'q' if "queenside castle" in opposite_player_moves else ''

    elif player == 'Black':
        WK_castle_flag = 'K' if "kingside castle" in opposite_player_moves else ''
        WQ_castle_flag = 'Q' if "queenside castle" in opposite_player_moves else ''

        BK_castle_flag = 'k' if "kingside castle" in all_moves else ''
        BQ_castle_flag = 'q' if "queenside castle" in all_moves else ''

    if WK_castle_flag == '' and WQ_castle_flag == '' and BK_castle_flag == '' and BQ_castle_flag == '':
        WK_castle_flag = '-'

    FEN_str = f"{"".join(str_arr)} {turn} {WK_castle_flag}{WQ_castle_flag}{BK_castle_flag}{BQ_castle_flag} {en_passant} {half_move_clock} {full_move_clock}"

    return FEN_str

def en_passant_check(piece_type, PieceInitPos, PieceFinalPos, player):
    InitRank, InitFile = PieceInitPos[0], PieceInitPos[1]
    FinalRank, FinalFile = PieceFinalPos[0], PieceFinalPos[1]

    if piece_type == 'p' or piece_type == 'P':
        if player == "White" and InitFile == FinalFile and InitRank == 6 and FinalRank == 4:
            return f"{Files[InitFile]}3"
        elif player == "Black" and InitFile == FinalFile and InitRank == 1 and FinalRank == 3:
            return f"{Files[InitFile]}6"

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