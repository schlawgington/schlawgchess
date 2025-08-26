from constants import *
from move import *
from helper import *

def score(BOARD_STATE, player_pieces, turn):
    white_material = 0
    black_material = 0

    for player in player_pieces.keys():
        for piece in player_pieces[player].keys():
            if player == 'white':
                white_material += Material_dict[player_pieces[player][piece]]
            else:
                black_material += Material_dict[player_pieces[player][piece].upper()]

    material_eval = white_material - black_material
    
    return material_eval

#def minimax(turn, cur_depth, position_score, target_depth)