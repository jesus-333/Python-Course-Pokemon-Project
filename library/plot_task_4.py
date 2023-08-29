import numpy as np
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def plot_health_during_fight(starter_list : list, battle_statistcs_per_starter : dict, max_number_of_turns : int):
    for starter in starter_list:
        # Get the list of hp during battle
        battle_statistcs = battle_statistcs_per_starter[starter]
        tmp_hp_during_battle = battle_statistcs['hp_during_battle']
        hp_during_battle = np.zeros((len(tmp_hp_during_battle), max_number_of_turns + 1)) # The +1 is present because in position 0 I always save the hp before the battle. Note that the hp are saved after the end of each turn

        for i in range(len(tmp_hp_during_battle)):
            hp_during_battle[i, 0:len(tmp_hp_during_battle[i])] = tmp_hp_during_battle[i]

        average_hp_during_battle = hp_during_battle.mean(0)
        std_hp_during_battle = hp_during_battle.std(0)
        turns = np.arange(max_number_of_turns + 1)

        fig, ax = plt.subplots(1, 1, figsize = (15, 10))

        ax.plot(turns, average_hp_during_battle)

        ax.set_title("Average %HP after battle")

        fig.tight_layout()
        fig.show()
               
