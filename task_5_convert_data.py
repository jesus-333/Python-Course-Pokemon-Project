import sys
import pickle

from library import pokemon_recomendation_system as prs

def load_data(starter_list : int, file_name : str, n_games : int, n_battles : int) -> dict:
    outcome_counter = dict()
    for starter in starter_list:
        pickle_in = open("results/{}_{}_{}_{}.pickle".format(file_name, starter, n_games, n_battles), "rb")
        outcome_counter_starter = pickle.load(pickle_in)
        outcome_counter[starter] = outcome_counter_starter
        pickle_in.close()

    return outcome_counter

def save_results(object_to_save, name):
    pickle_out = open("{}.pickle".format(name), "wb") 
    pickle.dump(object_to_save , pickle_out ) 
    pickle_out.close() 

if __name__ == '__main__':
    n_games = int( sys.argv[1] )
    n_battles = int( sys.argv[2] )

    starter_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    ml_data = load_data(starter_list, "ml_data", n_games, n_battles)

    ml_matrix, labels = prs.convert_ml_dict_to_matrix_and_labels(starter_list, ml_data)

    save_results(ml_matrix, "results/ml_matrix_{}_{}".format(n_games, n_battles))
    save_results(labels, "results/labels_{}_{}".format(n_games, n_battles))
