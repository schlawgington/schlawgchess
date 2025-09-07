from constants import *
from move import *
from board_eval import *
from helper import *
from pygui import *

def piece_move(opposite_player_moves, player_pieces, player, en_passant, BOARD):
    return_dict = {
        "init_pos_untranslated": None,
        "final_pos_untranslated": None,
        "init_pos_translated": None,
        "final_pos_translated": None,
        "all_legal_moves": None,
        "piece_type": None,
        "capture_flag": False,
        "checkmate_flag": False
    }

    if in_check(opposite_player_moves, player_pieces, player):
        print(f"{player} in check")
        all_legal_moves = moves_to_get_out_of_check(opposite_player_moves, opposite_player, player_pieces, player, BOARD, en_passant)

        if all_legal_moves == "CHECKMATE":
            return_dict["checkmate_flag"] = True
            return return_dict

        legal_moves_pieces = {}
        for piece in legal_moves.keys():
            if piece not in legal_moves_pieces:
                row, col = translate(piece)
                legal_move_pieces[piece] = BOARD[row][col].strip()

        untranslated_piece_to_move = get_in(legal_moves.keys())
        piece_init_pos = piece_init_row, piece_init_col = translate(untranslated_piece_to_move)

        untranslated_piece_move = get_in(legal_moves[untranslated_piece_to_move])
        piece_final_pos = piece_final_row, piece_final_col = translate(untranslated_piece_move)

    else:
        untranslated_piece_to_move = get_in(player_pieces[player])
        piece_init_pos = piece_init_row, piece_init_col = translate(untranslated_piece_to_move)

        all_legal_moves = {}
        for piece in player_pieces[player].keys():
            if piece not in all_legal_moves:
                all_legal_moves[piece] = legal_check(move(player_pieces, player, piece, BOARD, en_passant), player, opposite_player_moves)

        untranslated_piece_move = get_in(all_legal_moves[untranslated_piece_to_move])
        match untranslated_piece_move:
            case "kingside castle":
                piece_final_pos = piece_final_row, piece_final_col = (7, 6) if player == 'white' else (0, 6)
                pass
            case "queenside castle":
                piece_final_pos = piece_final_row, piece_final_col = (7, 2) if player == 'white' else (0, 2)
                pass
            case _:
                piece_final_pos = piece_final_row, piece_final_col = translate(untranslated_piece_move)

    if "PROMOTION" in untranslated_piece_move.upper():
        promotion = ['Q', 'R', 'N', 'B'] if player == "white" else ['q', 'r', 'n', 'b']
        promotion_in = get_in(promotion)
        BOARD[piece_init_row][piece_init_col] = f" {promotion_in} "

    return_dict["init_pos_untranslated"] = untranslated_piece_to_move
    return_dict["final_pos_untranslated"] = untranslated_piece_move
    return_dict["init_pos_translated"] = piece_init_pos
    return_dict["final_pos_translated"] = piece_final_pos
    return_dict["all_legal_moves"] = all_legal_moves
    return_dict["piece_type"] = BOARD[piece_init_row][piece_init_col]
    return_dict["capture_flag"] = True if (BOARD[piece_final_row][piece_final_col] != EMPTY or "ep" in untranslated_piece_to_move) else False

    return return_dict

def move_handling(BOARD, piece_init_pos, piece_final_pos, untranslated_piece_move, player):
    match untranslated_piece_move:
        case "queenside castle":
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
        case "kingside castle":
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
        case _:
            if "ep" not in untranslated_piece_move:
                BOARD[piece_final_pos[0]][piece_final_pos[1]] = BOARD[piece_init_pos[0]][piece_init_pos[1]]
                BOARD[piece_init_pos[0]][piece_init_pos[1]] = EMPTY
            else:
                if player == 'white':
                    BOARD[piece_final_pos[0]][piece_final_pos[1]] = BOARD[piece_init_pos[0]][piece_init_pos[1]]
                    BOARD[piece_final_pos[0] + 1][piece_final_pos[1]] = EMPTY
                
                else:
                    BOARD[piece_final_pos[0]][piece_final_pos[1]] = BOARD[piece_init_pos[0]][piece_init_pos[1]]
                    BOARD[piece_final_pos[0] - 1][piece_final_pos[1]] = EMPTY
                    
                BOARD[piece_init_pos[0]][piece_init_pos[1]] = EMPTY

initboard()
screen.blit(background, (0, 0))

def game_loop():
    game = True

    player = "white"
    opposite_player = "black"

    en_passant = '-'
    half_move_clock = 0
    full_move_clock = 1

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
        try:
            printboard(BOARD)

            player_pieces = get_pieces(BOARD)

            opposite_player_moves = []
            for piece in player_pieces[opposite_player].keys():
                opposite_player_moves.extend(move(player_pieces, opposite_player, piece, BOARD, en_passant))

            piece_move_return_dict = piece_move(opposite_player_moves, player_pieces, player, en_passant, BOARD)

            en_passant = en_passant_check(piece_move_return_dict["piece_type"], piece_move_return_dict["init_pos_untranslated"], piece_move_return_dict["final_pos_untranslated"], player)

            move_handling(BOARD, piece_move_return_dict["init_pos_translated"], piece_move_return_dict["final_pos_translated"], piece_move_return_dict["final_pos_untranslated"], player)
            
            if half_move_clock_check(piece_move_return_dict["piece_type"], piece_move_return_dict["capture_flag"]):
                half_move_clock = 0
            else:
                half_move_clock += 1

            if half_move_clock == 100:
                game = False
                print("Draw by 50 move rule")

            if player == "black":
                full_move_clock += 1

            FEN_str = FEN_str_gen(BOARD, player, piece_move_return_dict["all_legal_moves"], opposite_player_moves, en_passant, half_move_clock, full_move_clock)
            print(FEN_str)

            player = "black" if player == "white" else "white"
            opposite_player = "black" if player == "white" else "white"

            Drawboard(BOARD)

        except BackException:
            continue

game_loop()