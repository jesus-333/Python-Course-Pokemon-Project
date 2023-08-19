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

def get_specific_pokemon(pokemon_name : str, pokemon_file_path : str = 'data/pokemon_2.json'):
    pokemon_list = read_json(pokemon_file_path)
    
    for pokemon in pokemon_list: 
        if pokemon['name'] == pokemon_name: return pokemon

    raise ValueError("{} was not in the pokemon list of the file {}".format(pokemon_name, pokemon_file_path))

def get_specific_move(move_name: str, move_file_path : str = 'data/move_2.json'):
    move_list = read_json(move_file_path)
    
    for move in move_list: 
        if move['name'] == move_name: return move

    raise ValueError("{} was not in the pokemon list of the file {}".format(move, move_file_path))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Random creation of pokemon team and moves

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
        moves = get_random_pokemon(moves_file_path)
        
        # Create the pokemon and add to the team\
        pokemon_team.append(pokemon.Pokemon(pokemon_info, moves))

    return pokemon_team

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_started_pokemon(n_starter : int):
    if n_starter != 1 and n_starter != 2 and n_starter != 3:
        raise ValueError("n_starter must have value 1, 2 or 3")
    else:
        # Get moves and pokemon info from the files
        pokemon_list = read_json('data/pokemon_2.json')
        moves_list = read_json('data/moves_2.json')

        if n_starter == 1: # Bulbasaur
            starter_info = get_specific_pokemon('bulbasaur')
            moves = [get_specific_move('tackle',"razor leaf")]
        elif n_starter == 2:
            starter_info = get_specific_pokemon('charmender')
            moves = [get_specific_move('tackle',"ember")]
        elif n_starter == 3:
            starter_info = get_specific_pokemon('squirtle')
            moves = [get_specific_move('tackle',"water gun")]

        return pokemon.Pokemon(starter_info, moves)

