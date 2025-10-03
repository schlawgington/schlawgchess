from constants import *
from move import *
from helper import *
import threading
import gui
import queue

InputQueue = queue.Queue()

initboard(BOARD)

def game_loop():

    global player
    global opposite_player

    player = "white"
    opposite_player = "black"

    en_passant = '-'
    half_move_clock = 0
    full_move_clock = 1
    game = True

    pending_clicks = []

    while game:
        player_pieces = get_pieces(BOARD)

        opposite_player_moves = []
        for piece in player_pieces[opposite_player].keys():
            opposite_player_moves.extend(move(player_pieces, opposite_player, piece, BOARD, en_passant))

        piece_move_return_dict = piece_move(opposite_player_moves, player_pieces, player, opposite_player, en_passant, BOARD)

        all_legal_moves = GUIGetLegalMoves(opposite_player_moves, player_pieces, player, opposite_player, en_passant, BOARD)

        while not InputQueue.empty():
            pending_clicks.append(InputQueue.get())

            if len(pending_clicks) >= 2:
                piece_to_move_click = pending_clicks.pop(0)
                piece_move_location_click = pending_clicks.pop(0)

                if piece_to_move_click not in all_legal_moves.keys() or piece_move_location_click not in all_legal_moves[piece_to_move_click]:
                    continue
                else:
                    GUIMove(piece_to_move_click, piece_move_location_click)

        if piece_move_return_dict["checkmate_flag"]:
            print(f"{opposite_player} wins by checkmate")
            break

        en_passant = en_passant_check(
            piece_move_return_dict["piece_type"],
            piece_move_return_dict["init_pos_untranslated"],
            piece_move_return_dict["final_pos_untranslated"],
            player
        )

        move_handling(
            BOARD,
            piece_move_return_dict["init_pos_translated"],
            piece_move_return_dict["final_pos_translated"],
            piece_move_return_dict["final_pos_untranslated"],
            player
        )

        if half_move_clock_check(piece_move_return_dict["piece_type"], piece_move_return_dict["capture_flag"]):
            half_move_clock = 0
        else:
            half_move_clock += 1

        if half_move_clock == 100:
            game = False
            print("Draw by 50 move rule")

        if player == "black":
            full_move_clock += 1

        FEN_str = FEN_str_gen(
            BOARD,
            player,
            piece_move_return_dict["all_legal_moves"],
            opposite_player_moves,
            en_passant,
            half_move_clock,
            full_move_clock
        )
        
        player, opposite_player = opposite_player, player

threading.Thread(target=game_loop, daemon=True).start()

gui.pygameBoardLoop(BOARD, InputQueue)