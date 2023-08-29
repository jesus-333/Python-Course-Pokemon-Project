import numpy as np
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def plot_health_during_fight(starter_list : list, battle_statistcs_per_starter : dict, max_number_of_turns_per_starter : dict):
    fig, ax = plt.subplots(1, 1, figsize = (12, 8))

    for starter in starter_list:
        max_number_of_turns = max_number_of_turns_per_starter[starter]

        # Get the list of hp during battle
        battle_statistcs = battle_statistcs_per_starter[starter]
        tmp_hp_during_battle = battle_statistcs['hp_during_battle']
        hp_during_battle = np.zeros((len(tmp_hp_during_battle), max_number_of_turns + 1)) # The +1 is present because in position 0 I always save the hp before the battle. Note that the hp are saved after the end of each turn

        for i in range(len(tmp_hp_during_battle)):
            hp_during_battle[i, 0:len(tmp_hp_during_battle[i])] = tmp_hp_during_battle[i] / tmp_hp_during_battle[i][0]

        average_hp_during_battle = hp_during_battle.mean(0)
        std_hp_during_battle = hp_during_battle.std(0)
        turns = np.arange(max_number_of_turns + 1)


        ax.plot(turns, average_hp_during_battle, label = starter)
        ax.fill_between(turns, average_hp_during_battle + std_hp_during_battle, average_hp_during_battle - std_hp_during_battle, alpha = 0.2)

    ax.set_title("Average %HP after battle")
    ax.legend()
    ax.grid(True)
    ax.set_ylabel("% Health")
    ax.set_xlabel("N. Turns")
    ax.set_xlim([turns[0], turns[-1]])
    fig.tight_layout()
    fig.show()
               

def plot_pie_moves(starter_list : list, battle_statistcs_per_starter : dict):
    for starter in starter_list:
        battle_statistcs = battle_statistcs_per_starter[starter]
        
        damage_during_battle = battle_statistcs['damage_during_battle']
        moves_during_battle = battle_statistcs['moves_during_battle']
        
        # Compute the number of times each move was used and the total damage inflicted
        times_move_used = dict()
        tot_damage_by_move = dict()
        tot_damage_inflicted = 0
        for i in range(len(damage_during_battle)):
            damage_list = damage_during_battle[i]
            moves_list = moves_during_battle[i]
            for j in range(len(damage_list)):
                move = moves_list[j]
                damage = damage_list[j]

                if move not in times_move_used: times_move_used[move] = 1
                else: times_move_used[move] += 1

                if move not in tot_damage_by_move: tot_damage_by_move[move] = damage
                else: tot_damage_by_move[move] += damage

                tot_damage_inflicted += damage

        
        # Variable with the data for the plot
        x_1, x_2, labels  = [], [], []
        for move in times_move_used:
            x_1.append(times_move_used[move])       # Number of times each move was used
            x_2.append(tot_damage_by_move[move])    # tot damage done by each move
            labels.append(move)

        colors = plt.cm.prism(np.linspace(0, 1, len(x_1)))
        fig, axs = plt.subplots(1, 2, figsize = (16, 8))

        axs[0].pie(x_1, labels = labels, autopct='%1.1f%%', colors = colors)
        axs[0].set_title("# of times move used")

        axs[1].pie(x_2, labels = labels, autopct='%1.1f%%', colors = colors)
        axs[1].set_title("Damage by move")

        fig.suptitle("Information about moves - {}".format(starter))
        fig.tight_layout()
        fig.show()


def plot_pie_types(starter_list : list, wild_pokemon_encountered : dict, df_pokemon):
    # Count type json pokemon file
    n_pokemon_per_type_pokedex = dict()
    i = 1
    for types_list in df_pokemon['types']:
        for pokemon_type in types_list:
            if pokemon_type in n_pokemon_per_type_pokedex:
                n_pokemon_per_type_pokedex[pokemon_type] += 1
            else:
                n_pokemon_per_type_pokedex[pokemon_type] = 0
    
    for starter in starter_list:
        # Count type wild pokemon find
        n_pokemon_per_type_wild = dict()
        for wild_pokemon in wild_pokemon_encountered[starter]:
            types_list = df_pokemon[df_pokemon['name'] == wild_pokemon]['types'].iloc[0]
            for  pokemon_type in types_list:
                if pokemon_type in n_pokemon_per_type_wild:
                    n_pokemon_per_type_wild[pokemon_type] += 1
                else:
                    n_pokemon_per_type_wild[pokemon_type] = 0

        pokedex_types_distribution, pokedex_labels = compute_type_distribution(n_pokemon_per_type_pokedex)
        wild_types_distribution, wild_labels = compute_type_distribution(n_pokemon_per_type_wild)
        
        colors = plt.cm.rainbow(np.linspace(0, 1, len(pokedex_types_distribution)))
        fig, axs = plt.subplots(1, 2, figsize = (16, 8))

        axs[0].pie(pokedex_types_distribution, labels = pokedex_labels, autopct='%1.1f%%', colors = colors)
        axs[0].set_title("Types in JSON file")

        axs[1].pie(wild_types_distribution, labels = wild_labels, autopct='%1.1f%%', colors = colors)
        axs[1].set_title("Types wild pokemon")

        fig.suptitle("Information about types encountered - {}".format(starter))
        fig.tight_layout()
        fig.show()

def compute_type_distribution(types_dict : dict):
    type_distribution = []
    labels = []
    for pokemon_type in types_dict:
        type_distribution.append(types_dict[pokemon_type])
        labels.append(pokemon_type)

    return type_distribution, labels


def plot_bar_chart_damage(starter_list, battle_statistcs_per_starter : dict):
    fig, axs = plt.subplots(2, 2, figsize = (12, 8))
    idx_axs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    i = 0
    for starter in starter_list:
        battle_statistcs = battle_statistcs_per_starter[starter]

        damage_during_battle = battle_statistcs['damage_during_battle']
        level_during_battle = battle_statistcs['starter_level']
        
        damage_per_level = dict()
        for j in range(len(level_during_battle)):
            level = level_during_battle[j]
            damage = np.mean(damage_during_battle[j])

            if level in damage_per_level: 
                damage_per_level[level].append(damage)
            else:
                damage_per_level[level] = [damage]

        height = []
        labels = []
        for level in damage_per_level:
            # print(damage_per_level[level])
            height.append(np.mean(damage_per_level[level]))
            labels.append(int(level))
        
        x = np.arange(len(height))
        axs[idx_axs[i]].bar(x, height, label = labels)
        axs[idx_axs[i]].set_xlabel("Level")
        axs[idx_axs[i]].set_ylabel("Average Damage")
        axs[idx_axs[i]].set_title(starter)
        i += 1

    fig.suptitle("Average Damage per level")
    fig.tight_layout()
    fig.show()

        

