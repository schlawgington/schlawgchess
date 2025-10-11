from constants import *
from helper import *
from guiMOVE import *
import threading
import gui
import queue

InputQueue = queue.Queue()
MoveListQueue = queue.Queue()

initboard(BOARD)

def game_loop():

    global Player
    global OppositePlayer
    global game
    global MoveList

    Player = "White"
    OppositePlayer = "Black"

    en_passant = '-'
    half_move_clock = 0
    full_move_clock = 1
    game = True

    while game:
        MoveList = []
        Allpieces = GUIGetPieces(BOARD)

        #Unprocessed moves (eg can be legal or illegal)
        UnfilteredPlayerMoves = GetAllMoves(Allpieces, Player, BOARD, en_passant)
        OppositePlayerMoves = GetAllMoves(Allpieces, OppositePlayer, BOARD, en_passant)

        PlayerMoveBitBoard = CreatePieceMoveBitBoard(UnfilteredPlayerMoves, BOARD, Player)
        EnemyAttackBitBoard = CreatePieceMoveBitBoard(OppositePlayerMoves, BOARD, OppositePlayer)

        CheckDict = InCheck(EnemyAttackBitBoard, BOARD, Player)
        KingPos = CheckDict["King Position"]
        CheckBool = CheckDict["Check"]

        PinnedPieces = GetPinnedPieces(KingPos, BOARD, Player, OppositePlayer , Allpieces, UnfilteredPlayerMoves, en_passant, EnemyAttackBitBoard)

        PieceInitPos = InputQueue.get()
        if PieceInitPos == ContinueValue:
            continue
        
        TranslatedEnPassant = (8 - int(en_passant[1]), Filetonum[en_passant[0]]) if en_passant != '-' else None

        if CheckBool:
            legal_moves = InCheckMoveGeneration(PinnedPieces, Player, OppositePlayer, KingPos, BOARD, en_passant, EnemyAttackBitBoard)
            move_dict = legal_moves
        else:
            move_dict = PinnedPieces

        if PieceInitPos not in move_dict:
            continue

        valid_moves = move_dict[PieceInitPos]
        MoveListQueue.put(valid_moves)

        while True:
            PieceFinalPos = InputQueue.get()
            if PieceFinalPos == ContinueValue:
                break
            if PieceFinalPos in valid_moves:
                break
        
        if PieceFinalPos == ContinueValue:
            continue

        GUIMakeMove(PieceInitPos, PieceFinalPos, TranslatedEnPassant)

        AuxiliaryDict = GUIExtraStuffHandling(PieceInitPos, PieceFinalPos, BOARD)
        en_passant = en_passant_check(AuxiliaryDict["Piece Type"], PieceInitPos, PieceFinalPos, Player)
        
        Player, OppositePlayer = OppositePlayer, Player

threading.Thread(target=game_loop, daemon=True).start()

gui.pygameBoardLoop(BOARD, InputQueue, game, MoveListQueue)