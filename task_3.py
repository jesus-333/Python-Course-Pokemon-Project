import sys

from library import random_engine, plot_task_3

def main(n_game : int = 500, n_battles : int = 150):
    int_to_starter = ["pikachu", "bulbasaur", "charmandar", "squirtle"]

    wild_pokemon_encountered = dict()
    outcome_counter = dict()
    turns_per_battle = dict()
    percentage_hp_after_battle = dict()

    for i in range(4): # i go from 0 to 3 and represent the starter
        # Get the starter name
        starter = int_to_starter[i]

        # Dictionary initialization
        wild_pokemon_encountered[starter] = dict()
        outcome_counter[starter] = dict()
        turns_per_battle[starter] = np.zeros(n_game, n_battles)
        percentage_hp_after_battle[starter] = np.zeros(n_game, n_battles)

        for j in range(n_game):
            # Create game and simulate battles
            game = random_engine.Game(n_battles, i, 'data/pokemon_2.json', 'data/moves_2.json', 'data/type_effectiveness_2.json')
            tmp_wild_pokemon_encountered, tmp_outcome_counter, tmp_turns_per_battle, tmp_percentage_hp_after_battle = game.battle_to_simulate(n_battles)

            # Save statistics


if __name__ == '__main__':
    n_game = sys.argv[1]
    n_battles = sys.argv[2]
    main(n_game. n_battles)

