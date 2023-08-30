import pandas as pd
import numpy as np
import pickle

from . import Pokemon, Trainer, support
from . import pokemon_recomendation_system as prs
from .Battle import Battle

class Game():

    def __init__(self, pokemon_file_path : str, moves_file_path : str, effectiveness_file_path : str, encounter_prob : float = 0.8, keep_history : bool = False, selected_starter : int = -1):
        # Show if print the various menu/information.
        # Used only for the random mode

        # Save parameters
        self.print_var = True 
        if encounter_prob <= 0 or encounter_prob > 1: 
            raise ValueError("encounter_prob must be bigger than 0 and less or equal to 1")
        else: 
            self.encounter_prob = encounter_prob
        self.keep_history = keep_history
        
        # Dataframe with all the data of the json files
        self.df_pokemon = pd.read_json(pokemon_file_path)
        self.df_moves = pd.read_json(moves_file_path)
        self.df_effectiveness = pd.read_json(effectiveness_file_path)
    
        # Create the trainer
        if selected_starter == -1: # Create only in normale mode. selected_starter is different from -1 only in random mode
            self.create_trainer()

        try: 
            pickle_in = open("results/ml_model.pickle", "rb")
            self.ml_model = pickle.load(pickle_in)
            pickle_in.close()
        except:
            print("ML model not found")
            self.ml_model = None

    def create_trainer(self):
        support.clear()

        trainer_name = input("What is your name?\n")
        
        selected_pokemon = -1
        while selected_pokemon != 1 and selected_pokemon != 2 and selected_pokemon != 3:
            if not self.keep_history: support.clear()
            selected_pokemon = input("\nWhat is your starter?\n\t1) Bulbasaur\n\t2) Charmender\n\t3) Squirtle\n")
            if selected_pokemon.isnumeric(): selected_pokemon = int(selected_pokemon)

        if selected_pokemon == 1: starter = self.get_predefined_pokemon('bulbasaur')
        if selected_pokemon == 2: starter = self.get_predefined_pokemon('charmander')
        if selected_pokemon == 3: starter = self.get_predefined_pokemon('squirtle')
        
        self.trainer = Trainer.Trainer(trainer_name, [starter])
        if not self.keep_history: support.clear()

        if self.print_var:
            print(self.trainer)
            input("Print Enter to continue...")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def play_story(self):
        continute_game = True

        while continute_game:
            if not self.keep_history: support.clear()
            next_action = input(self.get_story_menu())

            if next_action.isnumeric():
                next_action = int(next_action)

                if next_action == 0: continute_game = False
                elif next_action == 1: self.explore()
                elif next_action == 2: self.pokemon_center()
                elif next_action == 3: self.pokemon_store()
                elif next_action == 4: print(self.trainer)
                else: print("Action not valid")

                input("Press Enter to continue...")

        print("Thanks for playing. The pokemon you search is in another region")

    def explore(self): 
        print("\nYou travel around the world")
        
        if np.random.rand() <= self.encounter_prob:
            # Select a random wild pokemon and create a fake trainer
            wild_pokemon = self.get_wild_pokemon()
            wild_trainer = Trainer.Trainer("Wild pokemon", [wild_pokemon])
        
            print("You find a wild pokemon")
            print("The wild pokemon is a wild {}".format(wild_pokemon.name))

            if self.ml_model is not None:
                for pokemon in self.trainer.pokemon_list:
                    probability = prs.predict_win_prob(pokemon.base_stats, wild_pokemon.types, self.ml_model) 
                    if probability[0] < 0.5:
                        print("{} has more than 50% of possibility to win the battle".format(pokemon.name))
                    else:
                        print("{} has less than 50% of possibility to win the battle".format(pokemon.name))
                input("Press Enter to continue...")

            battle = Battle(self.trainer, wild_trainer, use_ai_player_2 = True, keep_history = self.keep_history, df_effectiveness = self.df_effectiveness)
            battle_outcome = battle.battle()

            if battle_outcome == 1 or battle_outcome == 3:
                # 1 -> your pokemon win, 3 -> wild pokemon captured
                print("You win the battle")
            else:
                # 2 -> wild pokemon win
                print("You lose the battle. You run to pokemon center to cure your pokemon")
                self.pokemon_center()
        else:
            print("You find nothing trainer")

    def get_wild_pokemon(self):
        wild_pokemon_list = ["caterpie", "pidgey", "rattata"]
        wild_pokemon = self.get_predefined_pokemon(np.random.choice(wild_pokemon_list))
        print(wild_pokemon)

        return wild_pokemon

    def pokemon_center(self): 
        if self.print_var:
            print("\nYou visit the pokemon center")
            print("Your pokemons are fully healed and their pp recharged")

        for pokemon in self.trainer.pokemon_list:
            # Refill health
            pokemon.base_stats['hp'] = pokemon.base_stats['max_hp']
            
            # Refil moves pp
            for move in pokemon.moves: move.pp = move.max_pp

    def pokemon_store(self): 
        print("\nYou visit the pokemon store")
        print("You get 10 pokeballs and 10 potions")

        self.trainer.potion = 10
        self.trainer.pokeball = 10

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Methods to get information inside the json file (converted in pandas dataframe)

    def get_pokemon_info(self, pokemon_name : str):
        tmp_idx = self.df_pokemon['name'] == pokemon_name
        # Idx should be a boolean list with all false (0) and a signel true (1). So the sum must be 1 if the pokemon name is inside the dataframe
        if tmp_idx.sum() != 1:
            print("Pokemon name not valid")
            return None
        else:
            # Note that with this operation I obtain a dict of the following form {index : {dict with pokemon info}}
            raw_data = self.df_pokemon.loc[tmp_idx].to_dict(orient = 'index')
            # Operation to obtain the inside dictionary with the pokeon info
            pokemon_info = raw_data[list(raw_data.keys())[0]]
            return pokemon_info

    def get_move_info(self, move_name : str):
        tmp_idx = self.df_moves['name'] == move_name
        # Same as for the pokemon name
        if tmp_idx.sum() != 1:
            print("Move name not valid")
            return None
        else:
            raw_data = self.df_moves.loc[tmp_idx].to_dict(orient = 'index')
            moves_info = raw_data[list(raw_data.keys())[0]]

            return moves_info

    def get_predefined_pokemon(self, pokemon_name : str):
        # Get pokemon info from the pandas dataframe
        pokemon_info = self.get_pokemon_info(pokemon_name)
        
        # Get the predefined move for the pokemon
        moves_name = support.get_preset_moves(pokemon_name, True)
        moves = [self.get_move_info(move) for move in moves_name]
        
        return Pokemon.Pokemon(pokemon_info, moves) 

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def get_story_menu(self):
        menu_string = "Select what you want to do:\n"
        menu_string += "\t1) Explore\n"
        menu_string += "\t2) Pokemon center\n"
        menu_string += "\t3) Pokemon Store\n"
        menu_string += "\t4) Trainer info\n"

        menu_string += "\n\t0) Close game\n"

        return menu_string

