import random
import numpy as np

from . import game_engine, Battle, Pokemon

class random_game_engin(game_engine):

    def __init__(self, n_battles : int, pokemon_file_path : str, moves_file_path : str, effectivness_file_path : str):
        """
        Modified game engine to run the simulation
        """
        super().__init__(pokemon_file_path, moves_file_path, effectivness_file_path, 1, False)

        self.battle_to_simulate = n_battles
        
        self.clean_moves()
        self.print_var = False

    def simulate_battles(self):
        # Variable to save statistics 
        wild_pokemon_encountered = {}
        outcome_counter = dict( win = 0, loss = 0)
        turns_per_battle = np.zeros(self.battle_to_simulate)
        percentage_hp_after_battle = np.zeros(self.battle_to_simulate)

        for i in range(self.battle_to_simulate):
            # Spawn and fight wild pokemon
            wild_pokemon = self.get_wild_pokemon()
            battle = RandomBattle(self.trainer.pokemon_list[0], wild_pokemon)
            battle_outcome, turns = battle.execute_battle()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
            # Save statistics
            
            if wild_pokemon.name in wild_pokemon_encountered:
                wild_pokemon_encountered[wild_pokemon.name] += 1
            else:
                wild_pokemon_encountered[wild_pokemon.name] = 0

            if battle_outcome == 1: outcome_counter['win'] += 1
            elif battle_outcome == 2: outcome_counter['loss'] += 1

            turns_per_battle[i] = turns
            percentage_hp_after_battle[i] = self.trainer.pokemon_list[0].base_stats['hp'] /  self.trainer.pokemon_list[0].base_stats['max_hp']

        return wild_pokemon_encountered, outcome_counter, turns_per_battle, percentage_hp_after_battle

    def clean_moves(self):
        """
        Remove the moves with no power, i.e. all the moves that in json file have None has power
        """
        self.df_moves = self.df_moves[self.df_moves['power'].notna()]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Spawn pokemon methods

    def get_wild_pokemon(self):
        """
        Create a random wild pokemon
        """

        # Note that with this operation I obtain a dict of the following form {index : {dict with pokemon info}}
        raw_data = self.df_pokemon.sample().to_dict(orient = 'index')
        # Operation to obtain the inside dictionary with the pokeon info
        pokemon_info = raw_data[list(raw_data.keys())[0]]

        valid_moves = self.get_valid_moves(pokemon_info['types'])
        wild_pokemon = Pokemon.Pokemon(pokemon_info, valid_moves)

        return wild_pokemon
        
    
    def get_valid_moves(self, pokemon_types : list):
        """
        Create a list of all the moves corresponding to pokemon types + normal time and sample 2 moves randomly
        """
        pokemon_types.append('normal')
        list_valid_moves = self.df_moves[self.df_moves['type'].isin(pokemon_types)]
        return list_valid_moves.sample(2)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class RandomBattle(Battle):

    def __init__(self, pokemon_1 : "Pokemon", pokemon_2 : "Pokemon"):
        super().__init__([pokemon_1], [pokemon_2])

        self.pokemon_1 = pokemon_1
        self.pokemon_2 = pokemon_2

    def execute_battle(self):
        continue_battle = True
        turns = 0
        while continue_battle:
            # Select a random move for pokemon 1
            moves_1 = self.pokemon_1.moves
            idx_move_1 = random.randint(0, len(moves_1) - 1)
            
            # Select a random move for poekemon 2 
            moves_2 = self.pokemon_1.moves
            idx_move_2 = random.randint(0, len(moves_2) - 1)
            
            outcome = self.execute_both_move(idx_move_1, idx_move_2,)
            exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)

            self.recharge_pp(self.pokemon_1)
            self.recharge_pp(self.pokemon_2)

            turn += 1

        return exit_status_battle, turn

    def recharge_pp(self, pokemon : "Pokemon"):
        for move in pokemon.moves: move.pp = move.max_pp
