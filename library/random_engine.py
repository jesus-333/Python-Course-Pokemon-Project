from . import game_engine, Battle, Pokemon

class random_game_engin(game_engine):

    def __init__(self, n_battles : int, pokemon_file_path : str, moves_file_path : str, effectivness_file_path : str, encounter_prob : float = 0.8, keep_history : bool = False):
        """
        Modified game engine to run the simulation
        """
        super().__init__(pokemon_file_path, moves_file_path, effectivness_file_path, encounter_prob, keep_history)

        self.battle_to_simulate = n_battles

    def clean_moves(self,):
        """
        Remove the moves with no power, i.e. all the moves that in json file have None has power
        """
        self.df_moves = self.df_moves[self.df_moves['power'].notna()]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def get_wild_pokemon(self,):
        """
        Create a random wild pokemon
        """

        # Note that with this operation I obtain a dict of the following form {index : {dict with pokemon info}}
        raw_data = self.df_pokemon.loc[tmp_idx].to_dict(orient = 'index')
        # Operation to obtain the inside dictionary with the pokeon info
        pokemon_info = raw_data[list(raw_data.keys())[0]]

        valid_moves = self.get_valid_moves(pokemon_info['types'])
        wild_pokemon = Pokemon.Pokemon(pokemon_info, valid_moves)

        return wild_pokemon
        
    
    def get_valid_moves(self, pokemon_types : list):
        list_valid_moves = self.df_moves[self.df_moves['type'].isin(pokemon_types)]
        return list_valid_moves.sample(2)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class RandomBattle(Battle):

    def __init__(self):
        super().__init__()

