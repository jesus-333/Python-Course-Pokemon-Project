from numpy import floor

from . import Pokemon, support

class Battle():
    def __init__(self, pokemon_1 : "Pokemon" , pokemon_2 : "Pokemon", keep_history : bool = False):
        self.keep_history = keep_history

        self.pokemon_1 = pokemon_1
        self.pokemon_2 = pokemon_2

    def __battle(self):
        continue_battle = True

        while(continue_battle):
            if not self.keep_history: support.clear()

            



    def __get_menu_string(self):
        pass

    def __get_info_string(self):
        menu_string = ""

        menu_string += self.__get_pokemon_info_string(0)
        menu_string += "\n"
        menu_string += self.__get_pokemon_info_string(1)

        return menu_string


    def __get_pokemon_info_string(self, n_pokemon):
        pokemon = self.pokemon_1 if n_pokemon == 1 else self.pokemon_2
        current_hp = pokemon.base_stats['hp']
        max_hp = pokemon.base_stats['max_hp']

        percentage_hp = floor((current_hp / max_hp) * 10)

        info_string = "{} - L.{}".format(pokemon.name, pokemon.level)
        info_string += "-" * 12 + "\n"
        info_string += "|" + "#" * percentage_hp + " " * (10 - percentage_hp) + "|\t{}/{}".format(current_hp, max_hp)
        info_string += "-" * 12 + "\n"

        return info_string
