import matplotlib.pyplot as plt

def plot_n_victories(starter_list : list, outcome_counter : dict, n_games : int):
    total_win = []
    for starter in starter_list:
        total_win.append(outcome_counter[starter]['win'] / n_games) 

    fig, ax = plt.subplots(1, 1, figsize = (12, 8))

    ax.bar(starter_list, total_win)

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
