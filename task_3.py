import sys
import numpy as np
import pickle
import copy

from library import random_engine

def main(n_games : int = 500, n_battles : int = 150):
    starter_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]
    # starter_list = ["squirtle"]

    wild_pokemon_encountered = dict()
    outcome_counter = dict()
    turns_per_battle = dict()
    percentage_hp_after_battle = dict()

    for i in range(len(starter_list)): # i go from 0 to 3 and represent the starter
        # Get the starter name
        starter = starter_list[i]

        # Dictionary initialization
        wild_pokemon_encountered[starter] = dict()
        outcome_counter[starter] = dict(win = 0, loss = 0)
        turns_per_battle[starter] = np.zeros((n_games, n_battles))
        percentage_hp_after_battle[starter] = np.zeros((n_games, n_battles))

        for j in range(n_games):
            print(starter, round((j + 1)/n_games * 100, 2))

            # Create game and simulate battles
            game = random_engine.Game(n_battles, i, 'data/pokemon_2.json', 'data/moves_2.json', 'data/type_effectiveness_2.json')
            tmp_wild_pokemon_encountered, tmp_outcome_counter, tmp_turns_per_battle, tmp_percentage_hp_after_battle, _ = game.simulate_battles()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            # Save statistics

            # Wild pokemon encountered
            for wild_pokemon in tmp_wild_pokemon_encountered:
                if wild_pokemon not in wild_pokemon_encountered[starter]: # Wild pokemon not see in previous simulation
                    wild_pokemon_encountered[starter][wild_pokemon] = dict(
                        n_encounter = 1,
                        win = 0,
                        loss = 0,
                        percentage_hp_after_battle = [],
                        turns = []
                    )
                
                wild_pokemon_encountered[starter][wild_pokemon]['n_encounter'] = tmp_wild_pokemon_encountered[wild_pokemon]['n_encounter']
                wild_pokemon_encountered[starter][wild_pokemon]['win'] = tmp_wild_pokemon_encountered[wild_pokemon]['win']
                wild_pokemon_encountered[starter][wild_pokemon]['loss'] = tmp_wild_pokemon_encountered[wild_pokemon]['loss']
                wild_pokemon_encountered[starter][wild_pokemon]['percentage_hp_after_battle'].extend(tmp_wild_pokemon_encountered[wild_pokemon]['percentage_hp_after_battle']) 
                wild_pokemon_encountered[starter][wild_pokemon]['turns'].extend(tmp_wild_pokemon_encountered[wild_pokemon]['turns']) 

            # Battle outcome
            outcome_counter[starter]['win']  += tmp_outcome_counter['win']
            outcome_counter[starter]['loss'] += tmp_outcome_counter['loss']

            turns_per_battle[starter][j, :] = tmp_turns_per_battle
            percentage_hp_after_battle[starter][j, :] = tmp_percentage_hp_after_battle
        
        suffix = "_{}_{}_{}".format(starter, n_games, n_battles)
        save_results(wild_pokemon_encountered[starter], "results/wild_pokemon_encountered" + suffix)
        save_results(outcome_counter[starter], "results/outcome_counter" + suffix)
        save_results(turns_per_battle[starter], "results/turns_per_battle" + suffix)
        save_results(percentage_hp_after_battle[starter], "results/percentage_hp_after_battle" + suffix)

def save_results(object_to_save, name):
    pickle_out = open("{}.pickle".format(name), "wb") 
    pickle.dump(object_to_save , pickle_out ) 
    pickle_out.close() 

if __name__ == '__main__':
    n_games = int( sys.argv[1] )
    n_battles = int( sys.argv[2] )

    main(n_games, n_battles)

