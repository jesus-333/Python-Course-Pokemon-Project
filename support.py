import json
import random

import pokemon

"""
%load_ext autoreload
%autoreload 2
"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def read_json(path : str):
    # Open file and read data
    f = open(path)
    data = json.load(f)
    
    # Close file
    f.close()

    return data


def get_random_pokemon(pokemon_file_path : str, n_pokemon : int = 6):
    pokemon_data = read_json(pokemon_file_path)
    pokemon_list = random.sample(pokemon_data, n_pokemon)

    return pokemon_list


def get_random_moves(moves_file_path : str, n_moves : int = 4):
    moves_data = read_json(moves_file_path)
    moves_list = random.sample(moves_data, n_moves)

    return moves_list


def create_random_pokemon_team(pokemon_file_path : str, moves_file_path : str, n_pokemon : int = 6) -> list : 
    # Get a selection of random pokemon
    pokemon_list = get_random_pokemon(pokemon_file_path, n_pokemon)
    pokemon_team = []
    
    # For each pokemon info (saved in a dictionary) create the pokemon object and put in a list
    for pokemon_info in pokemon_list:
        # Get random moves for the pokemon
        # I know it is not efficient because I read the moves file everytime but I prefer this way for code clarity (also file are so small that performance should not be an issue)
        moves = get_random_moves(moves_file_path)
        
        # Create the pokemon and add to the team\
        pokemon_team.append(pokemon.Pokemon(pokemon_info, moves))

    return pokemon_list
