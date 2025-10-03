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

    while game:
        print(en_passant)
        player_pieces = get_pieces(BOARD)

        opposite_player_moves = []
        for piece in player_pieces[opposite_player].keys():
            opposite_player_moves.extend(move(player_pieces, opposite_player, piece, BOARD, en_passant))

        all_legal_moves = GUIGetLegalMoves(opposite_player_moves, player_pieces, player, opposite_player, en_passant, BOARD)
        if all_legal_moves == "CHECKMATE":
            game = False

        PieceInitPos = InitRow, InitCol = InputQueue.get()
        PieceFinalPos = FinalRow, FinalCol = InputQueue.get()

        if PieceInitPos not in all_legal_moves.keys() or PieceFinalPos not in all_legal_moves[PieceInitPos]:
            continue
        else:
            Capture_Pawn_Flag = GUIExtraStuffHandling(PieceInitPos, PieceFinalPos, BOARD)

            en_passant = en_passant_check(
                Capture_Pawn_Flag["Piece Type"],
                PieceInitPos,
                PieceFinalPos,
                player)

            if half_move_clock_check(Capture_Pawn_Flag["Piece Type"], Capture_Pawn_Flag["Capture Flag"]):
                half_move_clock = 0
            else:
                half_move_clock += 1

            if half_move_clock == 100:
                game = False

            GUIMove(PieceInitPos, PieceFinalPos)

        if player == "black":
            full_move_clock += 1

        FEN_str = FEN_str_gen(BOARD,
            player,
            all_legal_moves,
            opposite_player_moves,
            en_passant,
            half_move_clock,
            full_move_clock)

        player, opposite_player = opposite_player, player

threading.Thread(target=game_loop, daemon=True).start()

gui.pygameBoardLoop(BOARD, InputQueue)