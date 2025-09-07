from constants import *
from helper import *

def move(pieces:dict, color:str, user_in:str, BOARD, en_passant_availability):
    pos_moves = []
    cur_row = int(user_in[1])
    cur_file = Filetonum[user_in[0]]

    match pieces[color][user_in].upper():
        case 'P':
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

            if en_passant_availability != '-':
                if color == 'white' and en_passant_availability[1] == '6':
                    en_passant_file = Filetonum[en_passant_availability[0]]
                    if (cur_file == en_passant_file + 1 or cur_file == en_passant_file - 1) and cur_row == 5:
                        pos_moves.append(f"{en_passant_availability} ep")
            
                if color == 'black' and en_passant_availability[1] == '3':
                    en_passant_file = Filetonum[en_passant_availability[0]]
                    if (cur_file == en_passant_file + 1 or cur_file == en_passant_file - 1) and cur_row == 4:
                        pos_moves.append(f"{en_passant_availability} ep")

        case 'N':
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