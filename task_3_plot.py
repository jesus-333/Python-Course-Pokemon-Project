import sys
import numpy as np
import pickle

from library import  plot_task_3

def main(n_games : int, n_battles : int):
    int_to_starter = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    
    outcome_counter = load_data_outcome_counter(int_to_starter, n_games, n_battles)
    plot_task_3.plot_n_victories(int_to_starter, outcome_counter, n_games)


def load_data_outcome_counter(starter_list : int, n_games : int, n_battles : int) -> dict:
    outcome_counter = dict()
    for starter in starter_list:
        pickle_in = open("outcome_counter_{}_{}".format(n_games, n_battles))
        outcome_counter_starter = pickle.load(pickle_in)
        outcome_counter[starter] = outcome_counter_starter
        pickle_in.close()

    return outcome_counter

if __name__ == '__main__':
    main()
