from constants import *
from move import *
from board_eval import *
from helper import *

def game_loop(player, opposite_player):
    capture_flag = False

    printboard(BOARD)

    player_pieces = get_pieces(BOARD)

    cur_eval = score(BOARD, player_pieces, player)
    print(cur_eval)

    opposite_player_moves = []
    for piece in player_pieces[opposite_player].keys():
        opposite_player_moves.extend(move(player_pieces, opposite_player, piece, BOARD))

    if in_check(opposite_player_moves, player_pieces, player):
        print(f"{player} in check")
        legal_moves = moves_to_get_out_of_check(opposite_player_moves, opposite_player, player_pieces, player, BOARD)
        all_legal_moves = legal_moves

        if legal_moves == "CHECKMATE":
            return "CHECKMATE", None, None, None, None, None

        legal_move_pieces = {}
        for piece in legal_moves.keys():
            if piece not in legal_move_pieces:
                row, col = translate(piece)
                legal_move_pieces[piece] = BOARD[row][col].strip()

        print(legal_move_pieces)

        untranslated_piece_to_move = get_in(legal_moves.keys())
        if untranslated_piece_to_move.upper() == "BACK":
            return 1, None, None, None, None, None
        
        translated_piece_to_move = translate(untranslated_piece_to_move)

        print(legal_moves[untranslated_piece_to_move])

        untranslated_piece_move = get_in(legal_moves[untranslated_piece_to_move])
        if untranslated_piece_move.upper() == "BACK":
            return 1, None, None, None, None, None
        
        if "PROMOTION" in untranslated_piece_move:
            promotion = ['Q', 'R', 'N', 'B'] if player == "black" else ['q', 'r', 'n', 'b']
            print(promotion)
            promotion_in = get_in(promotion)
            BOARD[translated_piece_to_move[0]][translated_piece_to_move[1]] = f" {promotion_in} "
        
        translated_piece_move = translate(untranslated_piece_move)
    else:
        print(player_pieces[player])

        untranslated_piece_to_move = get_in(player_pieces[player])
        if untranslated_piece_to_move.upper() == "BACK":
            return 1, None, None, None, None, None

        translated_piece_to_move = translate(untranslated_piece_to_move)

        all_legal_moves = []
        for piece in player_pieces[player].keys():
            all_legal_moves.extend(move(player_pieces, player, piece, BOARD))

        legal_moves = legal_check(move(player_pieces, player, untranslated_piece_to_move, BOARD), player, opposite_player_moves)
        print(legal_moves)

        untranslated_piece_move = get_in(legal_moves)
        if untranslated_piece_move.upper() == "BACK":
            return 1, None, None, None, None, None
        
        if "PROMOTION" in untranslated_piece_move:
            promotion = ['Q', 'R', 'N', 'B'] if player == "black" else ['q', 'r', 'n', 'b']
            print(promotion)
            promotion_in = get_in(promotion)
            BOARD[translated_piece_to_move[0]][translated_piece_to_move[1]] = f" {promotion_in} "

        translated_piece_move = translate(untranslated_piece_move)
    
    if untranslated_piece_move == "QUEENSIDE CASTLE":
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

        FEN_str = FEN_str_gen(BOARD, player, all_legal_moves, opposite_player_moves)

        return 0, FEN_str, BOARD[translated_piece_move[0]][translated_piece_move[1]], untranslated_piece_to_move, untranslated_piece_move, capture_flag
    elif untranslated_piece_move == "KINGSIDE CASTLE":
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

        FEN_str = FEN_str_gen(BOARD, player, all_legal_moves, opposite_player_moves)

        return 0, FEN_str, BOARD[translated_piece_move[0]][translated_piece_move[1]], untranslated_piece_to_move, untranslated_piece_move, capture_flag
    else:
        if untranslated_piece_to_move in Castle_flags[player]:
            Castle_flags[player][untranslated_piece_to_move] = False

        if BOARD[translated_piece_move[0]][translated_piece_move[1]] != EMPTY:
            capture_flag = True

        BOARD[translated_piece_move[0]][translated_piece_move[1]] = BOARD[translated_piece_to_move[0]][translated_piece_to_move[1]]
        BOARD[translated_piece_to_move[0]][translated_piece_to_move[1]] = EMPTY

    FEN_str = FEN_str_gen(BOARD, player, all_legal_moves, opposite_player_moves)

    return 0, FEN_str, BOARD[translated_piece_move[0]][translated_piece_move[1]], untranslated_piece_to_move, untranslated_piece_move, capture_flag

initboard()

while game:
    status_code, mv_str, piece_type, piece_init_location, piece_final_location, capture_flag = game_loop(player, opposite_player)
    
    if status_code == 0:
        if half_move_clock_check(piece_type, capture_flag):
            half_move_clock = 0
        else:
            half_move_clock += 1

        if player == 'black':
            full_move_clock += 1

        if half_move_clock == 100:
            game = False
            print("Draw by 50 move rule")

        if isinstance(mv_str, str):
            new_str = f"{mv_str} {en_passant_check(piece_type, piece_init_location, piece_final_location, player)} {half_move_clock} {full_move_clock}"
            print(new_str)

        player = "black" if player == "white" else "white"
        opposite_player = "black" if player == "white" else "white"

    elif status_code == "CHECKMATE":
        game = False
        print(f"{opposite_player.upper()} wins!")