import pandas as pd
import numpy as np


def get_types_list(pokemon_json_path):
    """
    Get a list with all the type in the json file and a int for each type
    """
    types_list = []
    df_pokemon = pd.read_json(pokemon_json_path)
    for pokemon_types in df_pokemon['types']:
        for possible_type in pokemon_types:
            types_list.append(possible_type)

    unique_type_list = sort(set(types_list))
    # + 1 used to keep the 0 for no second type
    corresponding_int_for_type = np.arange(len(unique_type_list)) + 1

    type_to_int = dict()
    for i in range(len(unique_type_list)):
        type_to_int[unique_type_list[i]] = corresponding_int_for_type[i]

    return type_to_int

def convert_ml_dict_to_matrix(starter_list : list, ml_dict_per_starter : dict):
    type_to_int = get_types_list('data/pokemon_2.json')

    tmp_matrix = []
    for starter in starter_list:
        ml_dict = ml_dict_per_starter[starter]
        for battle in ml_dict:
            matrix_row = []

            matrix_row.append(battle['outcome'])

            for stats in ml_dict[battle]['pokemon_stats']: matrix_row.append(ml_dict[battle]['pokemon_stats'][stats]) 

            if len(ml_dict[battle]['enemy_types'] == 2):
                matrix_row.append(type_to_int[ml_dict[battle]['enemy_types'][0]])
                matrix_row.append(type_to_int[ml_dict[battle]['enemy_types'][1]])
            else:
                matrix_row.append(type_to_int[ml_dict[battle]['enemy_types'][0]])
                matrix_row.append(0)

        tmp_matrix.append(matrix_row)

    return np.asarray(tmp_matrix)
