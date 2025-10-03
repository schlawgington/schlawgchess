from constants import *
from helper import *

def move(pieces:dict, color:str, user_in:str, BOARD, en_passant_availability):
    pos_moves = []
    #Translate user input to numbers for offset calculations
    cur_row = int(user_in[1])
    cur_file = Filetonum[user_in[0]]

    match pieces[color][user_in].upper():
        case 'P':
            #Pawn capturing
            cap_directions = [(1, 1), (1, -1)] if color == "white" else [(-1, 1), (-1, -1)]
            for dr, df in cap_directions:
                if 0 <= cur_file + df < BOARD_WIDTH and 1 <= cur_row + dr <= BOARD_HEIGHT:
                    square = f"{Files[cur_file + df]}{cur_row + dr}"

                    if square in pieces["white" if color == "black" else "black"]:
                        if color == "white" and square[1] == '8':
                            pos_moves.append(f"{square} promotion")
                        elif color == "black" and square[1] == '1':
                            pos_moves.append(f"{square} promotion")
                        else:
                            pos_moves.append(square)

            #Pawn moving 2 squares from starting position
            match (cur_row, color):
                case (2, "white"):
                    offset = [1, 2]
                    for dr in offset:
                        square = f"{Files[cur_file]}{cur_row + dr}"

                        if square in pieces[color]:
                            break

                        else:
                            pos_moves.append(square)
                case (7, "black"):
                    offset = [-1, -2]
                    for dr in offset:
                        square = f"{Files[cur_file]}{cur_row + dr}"

                        if square in pieces[color]:
                            break

                        else:
                            pos_moves.append(square)
                case (2, "black"):
                    offset = -1
                    square = f"{Files[cur_file]}{cur_row + offset}"

                    if BOARD[BOARD_HEIGHT - cur_row - offset][cur_file] == EMPTY:
                        pos_moves.append(f"{square} promotion")
                case (7, "white"):
                    offset = 1
                    square = f"{Files[cur_file]}{cur_row + offset}"

                    if BOARD[BOARD_HEIGHT - cur_row - offset][cur_file] == EMPTY:
                        pos_moves.append(f"{square} promotion") 
                case _:
                    offset = -1 if color == "white" else 1
                    square = f"{Files[cur_file]}{cur_row - offset}"

                    if BOARD[BOARD_HEIGHT - cur_row + offset][cur_file] == EMPTY:
                        pos_moves.append(square)

            #En passant check
            if en_passant_availability != '-':
                if color == 'white' and en_passant_availability[1] == '6':
                    en_passant_file = Filetonum[en_passant_availability[0]]
                    if (cur_file == en_passant_file + 1 or cur_file == en_passant_file - 1) and cur_row == 5:
                        pos_moves.append(en_passant_availability)
            
                if color == 'black' and en_passant_availability[1] == '3':
                    en_passant_file = Filetonum[en_passant_availability[0]]
                    if (cur_file == en_passant_file + 1 or cur_file == en_passant_file - 1) and cur_row == 4:
                        pos_moves.append(en_passant_availability)

        case 'N':
            #Knight move generation
            directions = [
                (1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-1, 2),
                (-1, -2),
                (-2, 1),
                (-2, -1)
            ]

            for dr, df in directions:
                if 0 <= cur_file + df < BOARD_WIDTH and 1 <= cur_row + dr <= BOARD_HEIGHT:
                    square = f"{Files[cur_file + df]}{cur_row + dr}"
                    if square not in pieces[color]:
                        pos_moves.append(square)
        case 'B':
            #Bishop move generation
            directions = [
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1)
            ]

            for df, dr in directions:
                for offset in range(1, BOARD_HEIGHT):
                    file_idx = cur_file + df*offset
                    row_idx = cur_row + dr*offset

                    if not (0 <= file_idx < BOARD_WIDTH and 1 <= row_idx <= BOARD_HEIGHT):
                        break

                    square = f"{Files[file_idx]}{row_idx}"

                    if square in pieces[color]:
                        break

                    elif square in pieces["white" if color == "black" else "black"]:
                        pos_moves.append(square)
                        break

                    else:
                        pos_moves.append(square)
        case 'R':
            #Rook move generation
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            for df, dr in directions:
                for offset in range(1, BOARD_HEIGHT):
                    file_idx = cur_file + df*offset
                    row_idx = cur_row + dr*offset

                    if not (0 <= file_idx < BOARD_WIDTH and 1 <= row_idx <= BOARD_HEIGHT):
                        break

                    square = f"{Files[file_idx]}{row_idx}"

                    if square in pieces[color]:
                        break

                    elif square in pieces["white" if color == "black" else "black"]:
                        pos_moves.append(square)
                        break

                    else:
                        pos_moves.append(square)
        case 'Q':
            #Queen move generation
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1)
            ]

            for df, dr in directions:
                for offset in range(1, BOARD_HEIGHT):
                    file_idx = cur_file + df*offset
                    row_idx = cur_row + dr*offset

                    if not (0 <= file_idx < BOARD_WIDTH and 1 <= row_idx <= BOARD_HEIGHT):
                        break

                    square = f"{Files[file_idx]}{row_idx}"

                    if square in pieces[color]:
                        break

                    elif square in pieces["white" if color == "black" else "black"]:
                        pos_moves.append(square)
                        break

                    else:
                        pos_moves.append(square)
        case 'K':
            #King move generation
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1)
            ]

            for df, dr in directions:
                file_idx = cur_file + df
                row_idx = cur_row + dr

                if 0 <= file_idx < BOARD_WIDTH and 1 <= row_idx <= BOARD_HEIGHT:

                    square = f"{Files[file_idx]}{row_idx}"

                    if square in pieces[color]:
                        continue

                    elif square in pieces["white" if color == "black" else "black"]:
                        pos_moves.append(square)
                        continue

                    else:
                        pos_moves.append(square)

            #Check for castling possibility
            cur_king = "e1" if color == "white" else "e8"
            rook_pos = ["a1", "h1"] if color == "white" else ["a8", "h8"]
            queenside = ["c1", "d1"] if color == "white" else ["c8", "d8"]
            kingside = ["f1", "g1"] if color == "white" else ["f8", "g8"]

            if Castle_flags[color][cur_king]:
                if Castle_flags[color][rook_pos[0]] and all(sq not in pieces[color] for sq in queenside):
                    pos_moves.append("queenside castle")
                if Castle_flags[color][rook_pos[1]] and all(sq not in pieces[color] for sq in kingside):
                    pos_moves.append("kingside castle")
    
    return pos_moves

#Checks if castling is legal in current position
def legal_check(moves:list, player, opposite_player_moves):
    queenside = ["b1", "c1", "d1"] if player == "white" else ["b8", "c8", "d8"]
    kingside = ["e1", "f1", "g1"] if player == "white" else ["e8", "f8", "g8"]

    legal_moves = []
    for m in moves:
        if m == "queenside castle":
            if not any(sq in opposite_player_moves for sq in queenside):
                legal_moves.append(m)
        elif m == "kingside castle":
            if not any(sq in opposite_player_moves for sq in kingside):
                legal_moves.append(m)
        else:
            legal_moves.append(m)

    return legal_moves

#All moves to get out of check when check is detected
def moves_to_get_out_of_check(opposite_player_moves, opposite_player, player_pieces, player, BOARD, en_passant_availability):
    player_moves = {}
    legal_pieces = {}

    for piece in player_pieces[player].keys():
        if piece not in player_moves:
            player_moves[piece] = legal_check(move(player_pieces, player, piece, BOARD, en_passant_availability), player, opposite_player_moves)
        
        for mv in player_moves[piece]:
            init_row, init_col = translate(piece)
            final_row, final_col = translate(mv)

            BOARD_COPY = copy.deepcopy(BOARD)

            BOARD_COPY[final_row][final_col] = BOARD_COPY[init_row][init_col]
            BOARD_COPY[init_row][init_col] = EMPTY

            piece_dict = get_pieces(BOARD_COPY)

            opp_player_move_check = []
            for opp_piece in piece_dict[opposite_player].keys():
                opp_player_move_check.extend(move(piece_dict, opposite_player, opp_piece, BOARD_COPY, en_passant_availability))
           
            if not in_check(opp_player_move_check, piece_dict, player):
                if piece not in legal_pieces:
                    legal_pieces[piece] = [mv]
                else:
                    legal_pieces[piece].append(mv)

    if len(legal_pieces.keys()) == 0:
        return "CHECKMATE"

    return legal_pieces

def GUIGetLegalMoves(opposite_player_moves, player_pieces, player, opposite_player, en_passant, BOARD):
    if in_check(opposite_player_moves, player_pieces, player):
        all_legal_moves = moves_to_get_out_of_check(opposite_player_moves, opposite_player, player_pieces, player, BOARD, en_passant)

        if all_legal_moves == "CHECKMATE":
            return "CHECKMATE"
    else:
        all_legal_moves = {}
        for piece in player_pieces[player].keys():
            if piece not in all_legal_moves:
                all_legal_moves[piece] = legal_check(move(player_pieces, player, piece, BOARD, en_passant), player, opposite_player_moves)

    translated_legal_moves = {}

    for piece in all_legal_moves.keys():
        translated_piece = translate(piece)
        if translated_piece not in translated_legal_moves:
            translated_legal_moves[translated_piece] = [translate(piece_move) for piece_move in all_legal_moves[piece]]

    return translated_legal_moves

def GUIMove(PieceInitPos, PieceFinalPos):
    BOARD[PieceFinalPos[0]][PieceFinalPos[1]] = BOARD[PieceInitPos[0]][PieceInitPos[1]]
    BOARD[PieceInitPos[0]][PieceInitPos[1]] = EMPTY

def GUIExtraStuffHandling(PieceInitPos:tuple, PieceFinalPos:tuple, BOARD):
    return_dict = {
        "Piece Type": None,
        "Capture Flag": False
    }

    return_dict["Piece Type"] = BOARD[PieceInitPos[0]][PieceInitPos[1]].strip()

    if BOARD[PieceFinalPos[0]][PieceFinalPos[1]] != EMPTY:
        return_dict["Capture Flag"] = True

    return return_dict

#Handles user input for getting piece to move starting square and ending square
def piece_move(opposite_player_moves, player_pieces, player, opposite_player, en_passant, BOARD):
    #Dictionary containing all values needed for return in the game loop
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
        all_legal_moves = moves_to_get_out_of_check(opposite_player_moves, opposite_player, player_pieces, player, BOARD, en_passant)

        if all_legal_moves == "CHECKMATE":
            return_dict["checkmate_flag"] = True
            return return_dict

        print(f"{player} in check")

        legal_moves_pieces = {}
        for piece in all_legal_moves.keys():
            if piece not in legal_moves_pieces:
                row, col = translate(piece)
                legal_moves_pieces[piece] = BOARD[row][col].strip()

        untranslated_piece_to_move, untranslated_piece_move = piece_init_pos_to_final_pos(all_legal_moves)

        piece_init_pos = piece_init_row, piece_init_col = translate(untranslated_piece_to_move)
        piece_final_pos = piece_final_row, piece_final_col = translate(untranslated_piece_move)

    else:
        all_legal_moves = {}
        for piece in player_pieces[player].keys():
            if piece not in all_legal_moves:
                all_legal_moves[piece] = legal_check(move(player_pieces, player, piece, BOARD, en_passant), player, opposite_player_moves)
        
        untranslated_piece_to_move, untranslated_piece_move = piece_init_pos_to_final_pos(all_legal_moves)
        piece_init_pos = piece_init_row, piece_init_col = translate(untranslated_piece_to_move)

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

        while True:
            promotion_in = get_in(promotion)
            if promotion_in not in promotion:
                continue
            else:
                break

        BOARD[piece_init_row][piece_init_col] = f" {promotion_in} "

    return_dict["init_pos_untranslated"] = untranslated_piece_to_move
    return_dict["final_pos_untranslated"] = untranslated_piece_move
    return_dict["init_pos_translated"] = piece_init_pos
    return_dict["final_pos_translated"] = piece_final_pos
    return_dict["all_legal_moves"] = all_legal_moves
    return_dict["piece_type"] = BOARD[piece_init_row][piece_init_col]
    return_dict["capture_flag"] = True if (BOARD[piece_final_row][piece_final_col] != EMPTY or "ep" in untranslated_piece_to_move) else False

    return return_dict

#Handles kingside and queenside castling, en passant, and normal moves
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