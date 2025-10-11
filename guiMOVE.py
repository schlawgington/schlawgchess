from constants import *
from helper import *

def GUIGetPieces(BOARD_STATE):
    pieces= {"White": {}, "Black": {}}

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if BOARD_STATE[row][col].islower() and (row, col) not in pieces["Black"]:
                pieces["Black"][(row, col)] = BOARD[row][col].strip()
            elif BOARD_STATE[row][col].isupper() and (row, col) not in pieces["White"]:
                pieces["White"][(row, col)] = BOARD[row][col].strip()

    return pieces

def GUIMove(pieces: dict, piece, color: str, BoardState, EnPassant, debug = False):
    #Tuple of row, col: All possible moves (legal and illegal) in form of list of tuples
    PieceToMoveList = []
    OppositeColor = "White" if color == "Black" else "Black"

    PieceRow = piece[0]
    PieceFile = piece[1]

    if debug == True:
        breakpoint()
    match BoardState[PieceRow][PieceFile].strip().upper():
        case 'P':
            cap_directions = [(-1, 1), (-1, -1)] if color == "White" else [(1, 1), (1, -1)]
            for dr, df in cap_directions:
                if 0 <= PieceFile + df < BOARD_WIDTH and 0 <= PieceRow + dr < BOARD_HEIGHT:
                    CaptureSquare = (PieceRow + dr, PieceFile + df)

                    if CaptureSquare in pieces[OppositeColor]:
                        PieceToMoveList.append(CaptureSquare)

            match (PieceRow, color):
                case (1, "Black"):
                    offset = [1, 2]

                    for dr in offset:
                        Square = (PieceRow + dr, PieceFile)

                        if Square in pieces[color]:
                            break
                        else:
                            PieceToMoveList.append(Square)

                case (6, "White"):
                    offset = [-1, -2]

                    for dr in offset:
                        Square = (PieceRow + dr, PieceFile)

                        if Square in pieces[color]:
                            break
                        else:
                            PieceToMoveList.append(Square)

                case _:
                    offset = 1 if color == "Black" else -1

                    Square = (PieceRow + offset, PieceFile)

                    if BoardState[PieceRow + offset][PieceFile] == EMPTY:
                        PieceToMoveList.append(Square)
        
            if EnPassant != '-':
                EnPassantFile = Filetonum[EnPassant[0]]

                if color == "White" and PieceRow == 3 and (PieceFile + 1 == EnPassantFile or PieceFile - 1 == EnPassantFile) and BoardState[PieceRow - 1][EnPassantFile] == EMPTY:
                    Square = (2, EnPassantFile)
                    PieceToMoveList.append(Square)

                elif  color == "Black" and PieceRow == 4 and (PieceFile + 1 == EnPassantFile or PieceFile - 1 == EnPassantFile) and BoardState[PieceRow + 1][EnPassantFile] == EMPTY:
                    Square = (5, EnPassantFile)
                    PieceToMoveList.append(Square)

        case 'N':
        #Knight
            offsets = [
                (1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-1, 2),
                (-1, -2),
                (-2, 1),
                (-2, -1)
            ]

            for dr, df in offsets:
                if 0 <= PieceFile + df < BOARD_WIDTH and 0 <= PieceRow + dr < BOARD_HEIGHT:
                    Square = (PieceRow + dr, PieceFile + df)

                    if Square not in pieces[color]:
                        PieceToMoveList.append(Square)

        case 'B':
            offsets = [
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1)
            ]

            for dr, df in offsets:
                for offset in range(1, BOARD_HEIGHT):
                    RowIDX = dr*offset
                    FileIDX = df*offset

                    if 0 <= PieceFile + FileIDX < BOARD_WIDTH and 0 <= PieceRow + RowIDX < BOARD_HEIGHT:

                        Square = (PieceRow + RowIDX, PieceFile + FileIDX)

                        if Square in pieces[color]:
                            break

                        elif Square in pieces[OppositeColor]:
                            PieceToMoveList.append(Square)
                            break

                        else:
                            PieceToMoveList.append(Square)

        case 'R':
            offsets = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]                

            for dr, df in offsets:
                for offset in range(1, BOARD_HEIGHT):
                    RowIDX = dr*offset
                    FileIDX = df*offset

                    if 0 <= PieceRow + RowIDX < BOARD_HEIGHT and 0 <= PieceFile + FileIDX < BOARD_WIDTH:

                        Square = (PieceRow + RowIDX, PieceFile + FileIDX)

                        if Square in pieces[color]:
                            break

                        elif Square in pieces[OppositeColor]:
                            PieceToMoveList.append(Square)
                            break

                        else:
                            PieceToMoveList.append(Square)

        case 'Q':
            offsets = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1)
        ]

            for dr, df in offsets:
                for offset in range(1, BOARD_HEIGHT):
                    RowIDX = dr*offset
                    FileIDX = df*offset

                    if 0 <= PieceRow + RowIDX < BOARD_HEIGHT and 0 <= PieceFile + FileIDX < BOARD_WIDTH:

                        Square = (PieceRow + RowIDX, PieceFile + FileIDX)

                        if Square in pieces[color]:
                            break

                        elif Square in pieces[OppositeColor]:
                            PieceToMoveList.append(Square)
                            break

                        else:
                            PieceToMoveList.append(Square)

        case 'K':
            offsets = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1)
            ]
            
            for dr, df in offsets:
                RowIDX = dr + PieceRow
                FileIDX = df + PieceFile

                if 0 <= RowIDX < BOARD_HEIGHT and 0 <= FileIDX < BOARD_WIDTH:

                    Square = (RowIDX, FileIDX)

                    if Square in pieces[color]:
                        continue

                    elif Square in pieces[OppositeColor]:
                        PieceToMoveList.append(Square)
                        continue

                    else:
                        PieceToMoveList.append(Square)

            if color == "White":
                KingPosition = (7, 4)
                rook_pos   = [(7,0), (7,7)]
                queenside  = [(7,2), (7,3)]
                kingside   = [(7,5), (7,6)]
                KingsideCastlePos = (7, 6)
                QueensideCastlePos = (7, 2)
            else:
                KingPosition = (0, 4)
                rook_pos   = [(0,0), (0,7)]
                queenside  = [(0,2), (0,3)]
                kingside   = [(0,5), (0,6)]
                KingsideCastlePos = (0, 6)
                QueensideCastlePos = (0, 2)

            if GUICastleFlags[color][KingPosition]:
                if GUICastleFlags[color][rook_pos[0]] and all(sq not in pieces[color] for sq in queenside):
                    PieceToMoveList.append(QueensideCastlePos)
                if GUICastleFlags[color][rook_pos[1]] and all(sq not in pieces[color] for sq in kingside):
                    PieceToMoveList.append(KingsideCastlePos)

    return PieceToMoveList

def GetAllMoves(pieces, color, BoardState, EnPassant):
    PieceMoveDict = {}

    for piece in pieces[color]:
        PieceMoveDict[piece] = GUIMove(pieces, piece, color, BoardState, EnPassant)

    return PieceMoveDict

def InCheck(EnemyAttackingBitBoard, Board, color):
    KingCheckDict = {
        "Check": False,
        "King Position": None
    }

    King = 'K' if color == "White" else 'k'
    for Row in range(BOARD_HEIGHT):
        for Col in range(BOARD_WIDTH):
            if Board[Row][Col].strip() == King:
                KingCheckDict["King Position"] = (Row, Col)
                if EnemyAttackingBitBoard[Row][Col] == 1:
                    KingCheckDict["Check"] = True
            
    return KingCheckDict

def CreatePieceMoveBitBoard(PlayerMoveDict: dict, Board, Player: str): 
    Bitboard = [[0 for row in range(BOARD_HEIGHT)] for col in range(BOARD_WIDTH)]
    PawnCaptureOffsets = [(1, 1), (1, -1)] if Player == "Black" else [(-1, 1), (-1, -1)]

    for piece in PlayerMoveDict.keys():
        PieceRow, PieceCol = piece[0], piece[1]

        for PositionTuple in PlayerMoveDict[piece]:
            Row, Col= PositionTuple[0], PositionTuple[1]

            if Bitboard[Row][Col] == 1:
                continue
            elif Board[PieceRow][PieceCol].upper().strip() != 'P':
                Bitboard[Row][Col] = 1

        if Board[PieceRow][PieceCol].upper().strip() == 'P':
            for dr, df in PawnCaptureOffsets:
                if 0 <= PieceRow + dr < BOARD_HEIGHT and 0 <= PieceCol + df < BOARD_WIDTH and Bitboard[PieceRow + dr][PieceCol + df] != 1:
                    Bitboard[PieceRow + dr][PieceCol + df] = 1
                else:
                    continue

    return Bitboard

def KingAttackingLines(KingPos: tuple, Board, Player, OppositePlayer, EnPassant, debug = False, ForCheck = False):
    KingRow, KingCol = KingPos[0], KingPos[1]
    TestBoard = [row[:] for row in Board]
    
    PieceList = ['R', 'B'] if Player == "White" else ['r', 'b']
    Diagonals = ['Q', 'B'] if Player == "Black" else ['q', 'b']
    Straights = ['Q', 'R'] if Player == "Black" else ['q', 'r']

    Pieces = GUIGetPieces(TestBoard)

    AttackerToKingLineList = []

    for Piece in PieceList:
        TestBoard[KingRow][KingCol] = Piece

        CurrentPieceMoveList = GUIMove(Pieces, KingPos, Player, TestBoard, EnPassant)
        if len(CurrentPieceMoveList) == 0:
            continue

        for Position in CurrentPieceMoveList:
            Row, Col = Position[0], Position[1]
            if TestBoard[Row][Col] == EMPTY:
                continue

            EnemyPieceMoves = []

            if TestBoard[Row][Col].strip() in Diagonals:
                TestBoard[Row][Col] = 'B' if Player == "Black" else 'b'
                EnemyPieceMoves.extend(GUIMove(Pieces, (Row, Col), OppositePlayer, TestBoard, EnPassant))
            elif TestBoard[Row][Col].strip() in Straights:
                TestBoard[Row][Col] = 'R' if Player == "Black" else 'r'
                EnemyPieceMoves.extend(GUIMove(Pieces, (Row, Col), OppositePlayer, TestBoard, EnPassant))

            if len(EnemyPieceMoves) > 0:
                AttackerToKingLineList.extend(list(set(CurrentPieceMoveList) & set(EnemyPieceMoves)))
                AttackerToKingLineList.append((Row, Col))

    return list(set(AttackerToKingLineList))

def GetPinnedPieces(Kingpos: tuple, Board, Player, OppositePlayer, AllPieces, PlayerMoves, EnPassant, EnemyBitBoard):
    PinnedPieceMoveDict = {}
    PieceList = ['Q', 'R', 'B'] if OppositePlayer == "White" else ['q', 'r', 'b']
    OppositePlayerSlidingMoves = {}

    TestBoard = [[EMPTY for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
    TestBoard[Kingpos[0]][Kingpos[1]] = 'K' if Player == "White" else 'k'

    for Piece in AllPieces[OppositePlayer].keys():
        if AllPieces[OppositePlayer][Piece] in PieceList:
            Row, Col = Piece[0], Piece[1]
            TestBoard[Row][Col] = AllPieces[OppositePlayer][Piece]

    TestBoardPieces = GUIGetPieces(TestBoard)

    for Piece in TestBoardPieces[OppositePlayer].keys():
        PieceMoves = GUIMove(TestBoardPieces, Piece, OppositePlayer, TestBoard, '-')
        OppositePlayerSlidingMoves[Piece] = PieceMoves

    KingAttackingLinesList = KingAttackingLines(Kingpos, TestBoard, Player, OppositePlayer, EnPassant)

    for Piece, PieceMoves in PlayerMoves.items():
        if Piece == Kingpos:
            continue
        PieceRow, PieceCol = Piece[0], Piece[1]
        if Piece in KingAttackingLinesList and EnemyBitBoard[PieceRow][PieceCol] == 1:
            PinnedPieceMoveDict[Piece] = list(set(PieceMoves) & set(KingAttackingLinesList))
        else:
            PinnedPieceMoveDict[Piece] = PieceMoves

    for Row, Col in PlayerMoves[Kingpos]:
        PinnedPieceMoveDict[Kingpos] = PlayerMoves[Kingpos]
        if EnemyBitBoard[Row][Col] == 1:
            PinnedPieceMoveDict[Kingpos].remove((Row, Col))

    return PinnedPieceMoveDict

def InCheckMoveGeneration(FilteredPlayerMoves, Player, OppositePlayer, KingPos, Boardstate, EnPassant, EnemyBitBoard):
    LegalMoveDict = {}
    KingAttackingLinesList = KingAttackingLines(KingPos, Boardstate, Player, OppositePlayer, EnPassant, debug=True, ForCheck=True)

    for Piece, PieceMoves in FilteredPlayerMoves.items():
        if Piece == KingPos:
            continue
        LegalMoveList = list(set(PieceMoves) & set(KingAttackingLinesList))
        if len(LegalMoveList) > 0:
            LegalMoveDict[Piece] = LegalMoveList

    for Move in FilteredPlayerMoves[KingPos]:
        Row, Col = Move[0], Move[1]

        if EnemyBitBoard[Row][Col] == 1:
            FilteredPlayerMoves[KingPos].remove(Move)

    LegalMoveDict[KingPos] = FilteredPlayerMoves[KingPos]

    return LegalMoveDict

def GUIMakeMove(PieceInitPos, PieceFinalPos, EnPassant):
    InitRow, InitCol = PieceInitPos[0], PieceInitPos[1]
    FinalRow, FinalCol = PieceFinalPos[0], PieceFinalPos[1]

    match (PieceInitPos, PieceFinalPos, BOARD[InitRow][InitCol].strip()):
        case ((7, 4), (7, 6), 'K'):
            BOARD[7][6] = BOARD[7][4]
            BOARD[7][4] = EMPTY
            BOARD[7][5] = BOARD[7][7]
            BOARD[7][7] = EMPTY
        case ((7, 4), (7, 2), 'K'):
            BOARD[7][2] = BOARD[7][4]  
            BOARD[7][4] = EMPTY
            BOARD[7][3] = BOARD[7][0]  
            BOARD[7][0] = EMPTY
        case ((0, 4), (0, 6), 'k'):
            BOARD[0][6] = BOARD[0][4]  
            BOARD[0][4] = EMPTY
            BOARD[0][5] = BOARD[0][7] 
            BOARD[0][7] = EMPTY
        case ((0, 4), (0, 2), 'k'):
            BOARD[0][2] = BOARD[0][4]  
            BOARD[0][4] = EMPTY
            BOARD[0][3] = BOARD[0][0]
            BOARD[0][0] = EMPTY
        case _:
            if PieceFinalPos == EnPassant and BOARD[InitRow][InitCol].strip().lower() == 'p':
                EnPassantRow, EnPassantCol = EnPassant[0], EnPassant[1]

                direction = -1 if BOARD[InitRow][InitCol].isupper() else 1

                if (abs(InitCol - EnPassantCol) == 1 and InitRow == EnPassantRow - direction):

                    BOARD[EnPassantRow][EnPassantCol] = BOARD[InitRow][InitCol]
                    BOARD[InitRow][InitCol] = EMPTY

                    captured_pawn_row = EnPassantRow - direction
                    BOARD[captured_pawn_row][EnPassantCol] = EMPTY
            else:
                BOARD[FinalRow][FinalCol] = BOARD[InitRow][InitCol]
                BOARD[InitRow][InitCol] = EMPTY

def GUIExtraStuffHandling(PieceInitPos:tuple, PieceFinalPos:tuple, BOARD):
    return_dict = {
        "Piece Type": None,
        "Capture Flag": False
    }

    return_dict["Piece Type"] = BOARD[PieceFinalPos[0]][PieceFinalPos[1]].strip()

    if BOARD[PieceFinalPos[0]][PieceFinalPos[1]] != EMPTY:
        return_dict["Capture Flag"] = True

    return return_dict