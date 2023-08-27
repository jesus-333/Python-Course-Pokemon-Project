import matplotlib.pyplot as plt

def plot_n_victories(starter_list : list, outcome_counter : dict, n_games : int):
    total_win = []
    for starter in starter_list:
        total_win.append(outcome_counter[starter]['win'] / n_games) 

    fig, ax = plt.subplots(1, 1, figsize = (12, 8))

    ax.bar(starter_list, total_win)

    fig.tight_layout()
    plt.show()
