import sys
import pickle
import numpy as np

from library import  plot_task_3

def main(n_games : int, n_battles : int):
    starter_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    
    outcome_counter = load_data(starter_list, "outcome_counter", n_games, n_battles)
    plot_task_3.plot_n_victories(starter_list, outcome_counter, n_games)

    turns_per_battle = load_data(starter_list, "turns_per_battle", n_games, n_battles)
    percentage_hp_after_battle = load_data(starter_list, "percentage_hp_after_battle", n_games, n_battles)
    plot_task_3.box_plot_turns_and_residual_health(starter_list, turns_per_battle, percentage_hp_after_battle)

    for starter in starter_list:
        print("\n\nStarter", starter)
        print("\tTurns per battle:")
        print_statistics(turns_per_battle[starter].flatten())
        print("\tPercentage HP after battle:")
        print_statistics(percentage_hp_after_battle[starter].flatten())

    wild_pokemon_encountered = load_data(starter_list, "wild_pokemon_encountered", n_games, n_battles) 

    plot_task_3.bar_charts_percentage_victories(starter_list, wild_pokemon_encountered)

def load_data(starter_list : int, file_name : str, n_games : int, n_battles : int) -> dict:
    outcome_counter = dict()
    for starter in starter_list:
        pickle_in = open("results/{}_{}_{}_{}.pickle".format(file_name, starter, n_games, n_battles), "rb")
        outcome_counter_starter = pickle.load(pickle_in)
        outcome_counter[starter] = outcome_counter_starter
        pickle_in.close()

    return outcome_counter

def print_statistics(statistics):
    print("\t\tMean           = ", np.mean(statistics))
    print("\t\tMedian         = ", np.median(statistics))
    print("\t\t25th quartile = ", np.quantile(statistics, 0.25))
    print("\t\t75th quartile = ", np.quantile(statistics, 0.75))

if __name__ == '__main__':
    n_games = int( sys.argv[1] )
    n_battles = int( sys.argv[2] )

    main(n_games, n_battles)
    
    input("Press Enter to continue...")

