import numpy as np
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class Pokemon():

    def __init__(self, pokemon_info : dict, moves : list):
        self.national_pokedex_number = pokemon_info['national_pokedex_number']
        self.name = pokemon_info['name']
        self.types = pokemon_info['types']
        self.base_stats = pokemon_info['base_stats']
        
        self.check_moves(moves)
        self.moves = moves

        self.level = 1

        self.status = None

    def check_moves(self, moves : list):
        if len(moves) == len(set(moves)):
            print("Moves ok. No duplicates")
        else:
            raise ValueError("Duplicate moves")

    def use_move(self, idx_move : int, opponent : "Pokemon"):
        selected_move = self.moves[idx_move]
        
        # Check if there are enough pp
        if selected_move.pp > 0:

            # Check if the move hit the target
            if np.random.rand() <= self.accuracy: # Move hit the target
                # Compute modifier
                stability = 1.5 if selected_move.type in self.types else 1
                effect = 1
                critical = 2 if np.random.rand() < self.base_stats['speed'] / 512 else 1
                luck = np.random.uniform(0.85, 1)
                modifier = stability * effect * critical * luck
                
                # Get attack and defense
                attack = self.base_stats['attack'] if selected_move.category == 'physical' else self.base_stats['special']
                defense = opponent.base_stats['defense'] if selected_move.category == 'physical' else opponent.base_stats['special']

                # Compute damage
                base_damage = ((2 * self.level  + 10 ) / 250) * (attack / defense) * selected_move.power + 2
                damage = np.floor(base_damage * modifier)

                # print("{} hit the {}.".format(selected_move.name, opponent.name))
            else: # Move fails
                # print("{} fails".format(selected_move.name))
                damage = -1

            # Reduce pp
            selected_move.pp -= 1

        else: # Not enough pp
            damage = -2

        return selected_move, damage
        


class Move():
    def __init__(self, move_info : dict):
        self.name = move_info['name']
        self.type = move_info['type']
        self.category = move_info['category']
        self.power = move_info['power']
        self.accuracy = move_info['accuracy']
        self.pp = move_info['pp']
        self.effect = move_info['effect'] if type(move_info['effect']) == dict else None

