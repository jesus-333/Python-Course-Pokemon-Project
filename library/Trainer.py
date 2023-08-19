class Trainer():

    def __init__(self, name : str, pokemon_list : list):
        self.name = name
        self.pokemon_list = pokemon_list
        self.item = []


    def __str__(self):
        tmp_str = ""
        tmp_str += "My name is " + self.name + "\n"

        tmp_str += "My pokemon are:\n"
        for pokemon in self.pokemon_list: tmp_str += "\t" + pokemon.name + "\n"

        return tmp_str
