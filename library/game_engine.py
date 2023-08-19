import pandas as pd

from . import Pokemon, Trainer, support

class Game():

    def __init__(self, pokemon_file_path : str, moves_file_path : str):
        self.df_pokemon = pd.read_json(pokemon_file_path)
        self.df_moves = pd.read_json(moves_file_path)

    def play(self):
        self.create_trainer()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def create_trainer(self):
        support.clear()
        trainer_name = input("What is your name?\n")
        
        selected_pokemon = -1
        while selected_pokemon != 1 and selected_pokemon != 2 and selected_pokemon != 3:
            support.clear()
            selected_pokemon = input("\nWhat is your starter?\n\t1) Bulbasaur\n\t2) Charmender\n\t3) Squirtle\n")
            if selected_pokemon.isnumeric(): selected_pokemon = int(selected_pokemon)

        if selected_pokemon == 1: starter = self.get_predefined_pokemon('bulbasaur')
        if selected_pokemon == 2: starter = self.get_predefined_pokemon('charmander')
        if selected_pokemon == 3: starter = self.get_predefined_pokemon('squirtle')

        self.trainer = Trainer.Trainer(trainer_name, [starter])
        print(self.trainer)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def get_pokemon_info(self, pokemon_name : str):
        tmp_idx = self.df_pokemon['name'] == pokemon_name
        # Idx should be a boolean list with all false (0) and a signel true (1). So the sum must be 1 if the pokemon name is inside the dataframe
        if tmp_idx.sum() != 1:
            print("Pokemon name not valid")
            return None
        else:
            raw_data = self.df_pokemon.loc[tmp_idx].to_dict(orient = 'index')
            pokemon_info = raw_data[list(raw_data.keys())[0]]
            return pokemon_info

    def get_moves_info(self, move_name : str):
        tmp_idx = self.df_moves['name'] == move_name
        # Same as for the pokemon name
        if tmp_idx.sum() != 1:
            print("Move name not valid")
            return None
        else:
            return self.df_moves.loc[tmp_idx].to_dict()

    def get_predefined_pokemon(self, pokemon_name : str):
        # Get pokemon info from the pandas dataframe
        pokemon_info = self.get_pokemon_info(pokemon_name)
        
        # Get the predefined move for the pokemon
        moves = support.get_preset_moves(pokemon_name)

        return Pokemon.Pokemon(pokemon_info, moves)



