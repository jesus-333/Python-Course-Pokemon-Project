import json
import random
from os import system, name

from . import Pokemon

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

def get_specific_move(move_name: str, move_file_path : str = 'data/moves_2.json'):
    move_list = read_json(move_file_path)
    
    for move in move_list: 
        if move['name'] == move_name: return move

    raise ValueError("{} was not in the pokemon list of the file {}".format(move_name, move_file_path))

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
        pokemon_team.append(Pokemon.Pokemon(pokemon_info, moves))

    return pokemon_team

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_started_pokemon(n_starter : int):
    if n_starter != 1 and n_starter != 2 and n_starter != 3:
        raise ValueError("n_starter must have value 1, 2 or 3")
    else:
        if n_starter == 1: # Bulbasaur
            starter_info = get_specific_pokemon('bulbasaur')
            moves = get_preset_moves('bulbasaur')
        elif n_starter == 2: # Charmander
            starter_info = get_specific_pokemon('charmander')
            moves = get_preset_moves('charmander')
        elif n_starter == 3: #Squirtle
            starter_info = get_specific_pokemon('squirtle')
            moves = get_preset_moves('squirtle')

        return Pokemon.Pokemon(starter_info, moves)

def get_preset_moves(pokemon_name : str, return_only_names = False):
    """
    Given a pokemon name return some move(s) already defined
    """
    preset_pokemon_moves = dict(
        bulbasaur = ['tackle', 'razor leaf'],
        charmander = ['tackle', 'ember'],
        squirtle = ['tackle', 'water gun'],
        caterpie = ['twineedle'],
        pidgey = ['tackle', 'peck'],
        rattata = ['tackle']
    )
    
    if return_only_names:
        return preset_pokemon_moves[pokemon_name]
    else:
        moves = []
        for move in preset_pokemon_moves[pokemon_name]: moves.append(get_specific_move(move))

        return moves

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
