import random
import numpy as np
import copy

from . import game_engine, Battle, Pokemon, Trainer

class Game(game_engine.Game):

    def __init__(self, n_battles : int, starter : int, pokemon_file_path : str, moves_file_path : str, effectiveness_file_path : str):
        """
        Modified game engine to run the simulation
        n_battles = Number of random battle to simulate
        starter = int that specify  the starter to use (1 = bulbasaur, 2 = charmender, 3 = squirtle)
        """
        super().__init__(pokemon_file_path, moves_file_path, effectiveness_file_path, 1, False, starter)
        
        self.clean_moves()

        self.battle_to_simulate = n_battles
        self.print_var = False

        self.create_starter(starter)


    def create_starter(self, starter : int):
        int_to_starter = ["pikachu", "bulbasaur", "charmander", "squirtle"]
        pokemon_info = self.get_pokemon_info(int_to_starter[starter])

        valid_moves = self.get_valid_moves(copy.deepcopy(pokemon_info['types']))
        self.starter = Pokemon.Pokemon(pokemon_info, valid_moves)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def simulate_battles(self):
        # Variable to save statistics 
        wild_pokemon_encountered = {}
        outcome_counter = dict( win = 0, loss = 0)
        turns_per_battle = np.zeros(self.battle_to_simulate)
        percentage_hp_after_battle = np.zeros(self.battle_to_simulate)

        for i in range(self.battle_to_simulate):
            # Spawn and fight wild pokemon
            wild_pokemon = self.get_wild_pokemon()
            battle = RandomBattle(self.starter, wild_pokemon, self.df_effectiveness)
            battle_outcome, turns = battle.execute_battle()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
            # Save statistics
            
            if wild_pokemon.name in wild_pokemon_encountered:
                wild_pokemon_encountered[wild_pokemon.name]['n_encounter'] += 1
            else:
                wild_pokemon_encountered[wild_pokemon.name] = dict(
                    n_encounter = 1,
                    win = 0,
                    loss = 0,
                    percentage_hp_after_battle = [],
                    turns = []
                )

            if battle_outcome == 1: 
                outcome_counter['win'] += 1
                wild_pokemon_encountered[wild_pokemon.name]['win'] += 1
            elif battle_outcome == 2: 
                outcome_counter['loss'] += 1
                wild_pokemon_encountered[wild_pokemon.name]['loss'] += 1

            turns_per_battle[i] = turns
            percentage_hp_after_battle[i] = self.starter.base_stats['hp'] /  self.starter.base_stats['max_hp']

            wild_pokemon_encountered[wild_pokemon.name]['percentage_hp_after_battle'].append(percentage_hp_after_battle[i])
            wild_pokemon_encountered[wild_pokemon.name]['turns'].append(turns)

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            # Go to pokemon center to heal
            self.pokemon_center()


        return wild_pokemon_encountered, outcome_counter, turns_per_battle, percentage_hp_after_battle

    def clean_moves(self):
        """
        Remove the moves with no power, i.e. all the moves that in json file have None has power
        """
        self.df_moves = self.df_moves[self.df_moves['power'].notna()]


    def pokemon_center(self):
        # Refill health
        self.starter.base_stats['hp'] = self.starter.base_stats['max_hp']
        
        # Refil moves pp (not needed but put here just in case)
        for move in self.starter.moves: move.pp = move.max_pp

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
        tmp_type_list = ['normal']
        for pokemon_type in pokemon_types: tmp_type_list.append(pokemon_type)
        list_valid_moves = self.df_moves[self.df_moves['type'].isin(tmp_type_list)]
        valid_move = list_valid_moves.sample(2).to_dict(orient = 'index')

        return [valid_move[idx] for  idx in valid_move] 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class RandomBattle(Battle.Battle):

    def __init__(self, pokemon_1 : "Pokemon", pokemon_2 : "Pokemon", df_effectiveness):

        self.trainer_1 = Trainer.Trainer("Wild pokemon", [pokemon_1])
        self.trainer_2 = Trainer.Trainer("Wild pokemon", [pokemon_2])

        super().__init__(self.trainer_1, self.trainer_2, df_effectiveness = df_effectiveness)

    def execute_battle(self):
        continue_battle = True
        turns = 0
        while continue_battle:
            # Select a random move for pokemon 1
            moves_1 = self.trainer_1.pokemon_list[0].moves 
            idx_move_1 = random.randint(0, len(moves_1) - 1)
            
            # Select a random move for poekemon 2 
            moves_2 = self.trainer_2.pokemon_list[0].moves
            idx_move_2 = random.randint(0, len(moves_2) - 1)
            
            outcome = self.execute_both_moves(idx_move_1, idx_move_2, print_var = False)
            exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)

            self.recharge_pp(self.trainer_1.pokemon_list[0])
            self.recharge_pp(self.trainer_2.pokemon_list[0])

            turns += 1

        return exit_status_battle, turns

    def recharge_pp(self, pokemon : "Pokemon"):
        for move in pokemon.moves: move.pp = move.max_pp
