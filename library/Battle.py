import numpy as np

from . import Pokemon, support

class Battle():
    def __init__(self, pokemon_1 : "Pokemon" , pokemon_2 : "Pokemon", keep_history : bool = False):
        self.keep_history = keep_history

        self.pokemon_1 = pokemon_1
        self.pokemon_2 = pokemon_2

    def battle(self)-> int :
        continue_battle = True
        exit_status = 0

        while(continue_battle):
            if not self.keep_history: support.clear()
            
            # Print the pokeon info and the menu
            print(self.__get_info_string())
            selected_action = input(self.__get_main_menu_string())

            if selected_action.isnumeric():

                if int(selected_action) == 1: # Attack
                    pass
                elif int(selected_action) == 2: # Change pokemon
                    pass
                elif int(selected_action) == 3: # Use item
                    pass
                elif int(selected_action) == 4: # Run away
                    pass
                else:
                    print("Action not valid")

                input("Press Enter to continue...")
            
        return exit_status


    def __get_main_menu_string(self):
        menu_string = ""
        menu_string += "1) Attack\n"
        menu_string += "2) Change Pokemon\n"
        menu_string += "3) Use item\n"
        menu_string += "4) Run away\n"

        return menu_string

    def __get_info_string(self):
        info_string = ""

        info_string += self.__get_pokemon_info_string(0)
        info_string += "\n"
        info_string += self.__get_pokemon_info_string(1)

        return info_string


    def __get_pokemon_info_string(self, n_pokemon):
        pokemon = self.pokemon_1 if n_pokemon == 1 else self.pokemon_2
        current_hp = pokemon.base_stats['hp']
        max_hp = pokemon.base_stats['max_hp']

        percentage_hp = np.floor((current_hp / max_hp) * 10)

        info_string = "{} - L.{}".format(pokemon.name, pokemon.level)
        info_string += "-" * 12 + "\n"
        info_string += "|" + "#" * percentage_hp + " " * (10 - percentage_hp) + "|\t{}/{}".format(current_hp, max_hp)
        info_string += "-" * 12 + "\n"

        return info_string
