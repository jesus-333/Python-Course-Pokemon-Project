import matplotlib.pyplot as plt
import numpy as np

def plot_n_victories(starter_list : list, outcome_counter : dict, n_games : int):
    total_win = []
    for starter in starter_list:
        total_win.append(outcome_counter[starter]['win'] / n_games) 

    fig, ax = plt.subplots(1, 1, figsize = (12, 8))

    ax.bar(starter_list, total_win)
    ax.set_title("Average number of victories per game (n_games = {})".format(n_games))
    fig.tight_layout()
    fig.show()

def box_plot_turns_and_residual_health(starter_list : list, turns_per_battle : dict, percentage_hp_after_battle : dict):
    turn_list = []
    percentage_hp_list = []
    for starter in starter_list:
        turn_list.append(turns_per_battle[starter].flatten())
        percentage_hp_list.append(percentage_hp_after_battle[starter].flatten())

    fig, ax = plt.subplots(1, 1, figsize = (12, 8))
    ax.boxplot(turn_list, labels =  starter_list, patch_artist = True)
    ax.set_title("Turns per battle")
    fig.tight_layout()
    fig.show()

    fig, ax = plt.subplots(1, 1, figsize = (12, 8))
    ax.boxplot(percentage_hp_list, labels = starter_list)
    ax.set_title("Percentage HP after battle")
    fig.tight_layout()
    fig.show()

def bar_charts_percentage_victories(starter_list : list, wild_pokemon_encountered : dict):
    for starter in starter_list:
        wild_pokemon_list = []
        percentage_victories = []
        turns_list = []
        for wild_pokemon in wild_pokemon_encountered[starter]:
            wild_pokemon_list.append(wild_pokemon)
            percentage_victories.append(wild_pokemon_encountered[starter][wild_pokemon]['win'] / (wild_pokemon_encountered[starter][wild_pokemon]['win'] + wild_pokemon_encountered[starter][wild_pokemon]['loss']))
            turns_list.extend(wild_pokemon_encountered[starter][wild_pokemon]['turns'])
        
        color = []
        for i in range(len(wild_pokemon_list)):
            wild_pokemon = wild_pokemon_list[i]
            if percentage_victories[i] > 0.7: 
                if wild_pokemon_encountered[starter][wild_pokemon]['percentage_hp_after_battle'].mean() > 0.7:
                    color.append('green')
                else:
                    color.append('blue')
            else: 
                if wild_pokemon_encountered[starter][wild_pokemon]['turns'] >= np.median(turns_list):
                    color.append('red')
                else:
                    color.append('blue')

        fig, ax = plt.subplots(1, 1, figsize = (18, 8))
        
        x = np.arange(len(wild_pokemon_list))
        ax.bar(x, percentage_victories)

        ax.set_xticks(x, wild_pokemon_list, rotation = 90)
        for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), color):
            ticklabel.set_color(tickcolor)

        ax.set_title("Percentage victory for encounter: {}".format(starter))

        fig.tight_layout()
        fig.show()
