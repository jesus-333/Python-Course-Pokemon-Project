import numpy as np

class Pokemon():

    def __init__(self, national_pokedex_number : int, name : str, types : list, base_stats : dict, moves : list):
        self.national_pokedex_number = national_pokedex_number
        self.name = name
        self.types = types
        self.base_stats = base_stats
        
        self.check_moves(moves)
        self.moves = moves

        self.level = 1

        self.status = None

    def check_moves(self, moves : list):
        if len(moves) == len(set(moves)):
            print("Moves ok. No duplicates")
        else:
            raise ValueError("Duplicate moves")

    def use_move(self, idx_move : int, opponent : Pokemon):
        


class Move():
    def __init__(self, move_info : dict):
        self.name = move_info['name']
        self.type = move_info['type']
        self.category = move_info['category']
        self.power = move_info['power']
        self.accuracy = move_info['accuracy']
        self.pp = move_info['pp']
        self.effect = move_info['effect'] if type(move_info['effect']) == dict else None

