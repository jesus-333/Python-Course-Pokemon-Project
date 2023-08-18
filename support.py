import json

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def read_json(path : str):
    # Open file and read data
    f = open(path)
    data = json.load(f)
    
    # Close file
    f.close()

    return data


def get_random_pokemon(n_pokemon : int = 6):
    pass
