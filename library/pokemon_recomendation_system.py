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
    
    unique_type_list = np.sort(list(set(types_list)))
    # + 1 used to keep the 0 for no second type
    corresponding_int_for_type = np.arange(len(unique_type_list)) + 1

    type_to_int = dict()
    for i in range(len(unique_type_list)):
        type_to_int[unique_type_list[i]] = corresponding_int_for_type[i]

    return type_to_int

def convert_ml_dict_to_matrix_and_labels(starter_list : list, ml_dict_per_starter : dict):
    type_to_int = get_types_list('data/pokemon_2.json')

    tmp_matrix = np.zeros((len(ml_dict_per_starter[starter_list[0]]['battle_outcome']) * len(starter_list), 7))
    labels = []
    idx = 0
    for starter in starter_list:
        ml_dict = ml_dict_per_starter[starter]
        
        for i in range(len(ml_dict['battle_outcome'])):
            print(idx)
            labels.append(ml_dict['battle_outcome'][i]) 

            for stats_dict in ml_dict['pokemon_stats']: 
                k = 0
                for stats in stats_dict: 
                    if stats != 'max_hp': 
                        tmp_matrix[idx, k] = stats_dict[stats] 
                        k += 1

            if len(ml_dict['enemy_types'][i]) == 2:
                tmp_matrix[idx, 5] = type_to_int[ml_dict['enemy_types'][i][0]]
                tmp_matrix[idx, 6] = type_to_int[ml_dict['enemy_types'][i][1]]
            else:
                tmp_matrix[idx, 5] = type_to_int[ml_dict['enemy_types'][i][0]]
                tmp_matrix[idx, 6] = 0

            idx += 1

    return tmp_matrix, labels
