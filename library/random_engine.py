from . import game_engine, Battle, Pokemon

class random_game_engin(game_engine):

    def __init__(self, n_battles : int, pokemon_file_path : str, moves_file_path : str, effectivness_file_path : str):
        """
        Modified game engine to run the simulation
        """
        super().__init__(pokemon_file_path, moves_file_path, effectivness_file_path, 1, False)

        self.battle_to_simulate = n_battles
        
        self.clean_moves()

    def clean_moves(self,):
        """
        Remove the moves with no power, i.e. all the moves that in json file have None has power
        """
        self.df_moves = self.df_moves[self.df_moves['power'].notna()]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Spawn pokemon methods

    def get_wild_pokemon(self,):
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

    def __init__(self):
        super().__init__()

    def compute_effectivness(self, attacker : "Pokemon", defender : "Pokemon") -> float :
        effect = 1
        for attacker_type in attacker.types:
            for defender_type in defender.types:
                attacker_filter = (self.df_effectivness['attack'] == attacker_type)
                defender_filter = (self.df_effectivness['defend'] == defender_type)
                effect *= self.df_effectivness[attacker_filter & defender_filter]

        return effect
