import sys
import pickle
import numpy as np

from library import pokemon_recomendation_system as prs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def load_data(file_name : str, n_games : int, n_battles : int) -> dict:
    pickle_in = open("results/{}_{}_{}.pickle".format(file_name, n_games, n_battles), "rb")
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data

def save_results(object_to_save, name):
    pickle_out = open("{}.pickle".format(name), "wb") 
    pickle.dump(object_to_save , pickle_out ) 
    pickle_out.close() 

if __name__ == '__main__':
    n_games = int( sys.argv[1] )
    n_battles = int( sys.argv[2] )

    starter_list = [""]
    ml_data = load_data("ml_matrix", n_games, n_battles)
    labels = np.array(load_data("labels", n_games, n_battles))

    ml_model = LinearDiscriminantAnalysis()
    ml_model.fit(ml_data, labels)
    print(ml_model.score(ml_data, labels))

    save_results(ml_model, "results/ml_model")
