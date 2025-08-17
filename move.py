from constants import *

def move(pieces:dict, color:str, user_in:str, BOARD):
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
                case _:
                    offset = 1 if color == "white" else -1
                    square = f"{Files[cur_file]}{cur_row + offset}"

                    if BOARD[BOARD_HEIGHT - cur_row + offset][cur_file] == ' . ':
                        pos_moves.append(square)
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

            cur_king = "E1" if color == "white" else "E8"
            rook_pos = ["A1", "H1"] if color == "white" else ["A8", "H8"]
            queenside = ["C1", "D1"] if color == "white" else ["C8", "D8"]
            kingside = ["F1", "G1"] if color == "white" else ["F8", "G8"]

            if Castle_flags[color][cur_king]:
                if Castle_flags[color][rook_pos[0]] and all(sq not in pieces[color] for sq in queenside):
                    pos_moves.append("QUEENSIDE CASTLE")
                if Castle_flags[color][rook_pos[1]] and all(sq not in pieces[color] for sq in kingside):
                    pos_moves.append("KINGSIDE CASTLE")
    
    return pos_moves

def legal_check(moves:list, player, opposite_player_moves):
    queenside = ["B1", "C1", "D1"] if player == "white" else ["B8", "C8", "D8"]
    kingside = ["E1", "F1", "G1"] if player == "white" else ["E8", "F8", "G8"]

    legal_moves = []
    for m in moves:
        if m == "QUEENSIDE CASTLE":
            if all(sq not in opposite_player_moves for sq in queenside):
                legal_moves.append(m)
        elif m == "KINGSIDE CASTLE":
            if all(sq not in opposite_player_moves for sq in kingside):
                legal_moves.append(m)
        else:
            legal_moves.append(m)

    print(legal_moves)

    return legal_moves