from constants import *
from move import *
from helper import *

def score(FEN_str, player_pieces, all_legal_moves, opposite_player_moves, cur_player):
    white_material = 0
    black_material = 0

    current_player_modifier = 1 if cur_player == 'white' else -1
    opposite_player_modifier = -1 if cur_player == 'white' else 1 

    for player in player_pieces.keys():
        for piece in player_pieces[player].keys():
            if player == 'white':
                white_material += Material_dict[player_pieces[player][piece]]
            else:
                black_material -= Material_dict[player_pieces[player][piece].upper()]

    material_eval = white_material + black_material
    
    mobility_eval = current_player_modifier*len(all_legal_moves) + opposite_player_modifier*len(opposite_player_moves)

    tot_eval = material_eval +  0.1*mobility_eval

    return tot_eval

#def minimax(turn, cur_depth, position_score, target_depth)