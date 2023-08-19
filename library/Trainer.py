class Trainer():

    def __init__(self, name : str, pokemon_list : list):
        self.name = name
        self.pokemon_list = pokemon_list

        self.items = dict(
            potion = 10,
            pokebal = 10
        )

    def __str__(self):
        tmp_str = ""
        tmp_str += "My name is " + self.name + "\n\n"

        tmp_str += "* * " * 20 + "\n"

        tmp_str += "My pokemons are:\n\n"
        # for pokemon in self.pokemon_list: tmp_str += "\t{} {}/{}hp\n".format(pokemon.name, pokemon.base_stats['hp'], pokemon.base_stats['max_hp'])
        for pokemon in self.pokemon_list: tmp_str += "\t{}\n".format(pokemon.get_string_description().replace("\n", "\n\t"))
        
        tmp_str += "* * " * 20 + "\n"
        tmp_str += "\nMy item are:\n"
        for item_name in self.items: tmp_str += "\t{} : {}\n".format(item_name, self.items[item_name])

        return tmp_str
