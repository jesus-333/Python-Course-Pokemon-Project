import sys
import pickle
import numpy as np
import pandas as pd

from library import  plot_task_4

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

    starter_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    
    outcome_counter = load_data(starter_list, "outcome_counter", n_games, n_battles)
    turns_per_battle = load_data(starter_list, "turns_per_battle", n_games, n_battles)
    percentage_hp_after_battle = load_data(starter_list, "percentage_hp_after_battle", n_games, n_battles)
    wild_pokemon_encountered = load_data(starter_list, "wild_pokemon_encountered", n_games, n_battles) 
    battle_statistics = load_data(starter_list, "battle_statistics", n_games, n_battles)
    
    max_number_of_turns_per_starter = dict()
    for starter in starter_list: max_number_of_turns_per_starter[starter] = int(turns_per_battle[starter].max())
    plot_task_4.plot_health_during_fight(starter_list , battle_statistics , max_number_of_turns_per_starter)

    plot_task_4.plot_pie_moves(starter_list, battle_statistics)

    df_pokemon = pd.read_json('data/pokemon_2.json')
    plot_task_4.plot_pie_types(starter_list, wild_pokemon_encountered, df_pokemon)

    plot_task_4.plot_bar_chart_damage(starter_list, battle_statistics)
    
    input("Press Enter to continue...")