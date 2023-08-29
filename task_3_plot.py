import sys
import pickle

from library import  plot_task_3

def main(n_games : int, n_battles : int):
    int_to_starter = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    
    outcome_counter = load_data(int_to_starter, "outcome_counter", n_games, n_battles)
    plot_task_3.plot_n_victories(int_to_starter, outcome_counter, n_games)

    turns_per_battle = load_data(int_to_starter, "turns_per_battle", n_games, n_battles)
    percentage_hp_after_battle = load_data(int_to_starter, "percentage_hp_after_battle", n_games, n_battles)
    plot_task_3.box_plot_turns_and_residual_health(int_to_starter, turns_per_battle, percentage_hp_after_battle)

    print(turns_per_battle['bulbasaur'])
    import numpy as np
    print(np.max(turns_per_battle['bulbasaur']))
    print(np.min(turns_per_battle['bulbasaur']))

    wild_pokemon_encountered = load_data(int_to_starter, "wild_pokemon_encountered", n_games, n_battles) 

def load_data(starter_list : int, file_name : str, n_games : int, n_battles : int) -> dict:
    outcome_counter = dict()
    for starter in starter_list:
        pickle_in = open("results/{}_{}_{}_{}.pickle".format(file_name, starter, n_games, n_battles), "rb")
        outcome_counter_starter = pickle.load(pickle_in)
        outcome_counter[starter] = outcome_counter_starter
        pickle_in.close()

    return outcome_counter

if __name__ == '__main__':
    n_games = int( sys.argv[1] )
    n_battles = int( sys.argv[2] )

    main(n_games, n_battles)

