import numpy as np

from . import support

class Battle():
    def __init__(self, trainer_1, trainer_2, use_ai_player_1 = True, keep_history : bool = False):
        self.keep_history = keep_history
        self.use_ai_player_1 = use_ai_player_1

        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2

        self.current_pokemon_1 = self.trainer_1.pokemon_list[0]
        self.current_pokemon_2 = self.trainer_2.pokemon_list[0]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

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
                    selecte_move_idx_1 = self.attack(1)
                elif int(selected_action) == 2: # Change pokemon
                    pass
                elif int(selected_action) == 3: # Use item
                    pass
                elif int(selected_action) == 4: # Run away
                    if np.random.rand() <= 0.6:
                        print("\nYou ran away")
                        continue_battle = False
                        exit_status = 4
                        continue
                    else:
                        print("You can't run away")
                else:
                    print("Action not valid")
            else:
                print("Action not valid")

            input("Press Enter to continue...")
            
        print("The battle is over.")
        return exit_status

    def attack(self, n_pokemon : int):
        menu_string = self.__get_moves_menu(n_pokemon)
        continute_selection = True
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2

        while continute_selection:
            if not self.keep_history: support.clear()
            selected_move = input(menu_string)

            if selected_move.isnumeric():
                selected_move = int(selected_move)

                # To obtain a valid index remove 1
                selected_move -= 1

                # Check the input
                # if -1 it means exit otherwise is the index of the move
                if selected_move >= -1 and selected_move < len(pokemon.moves): 
                    continute_selection = False
                else:
                    print("Action not valid")

        return selected_move


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Main battle menu

    def __get_main_menu_string(self) -> str:
        menu_string = ""
        menu_string += "1) Attack\n"
        menu_string += "2) Change Pokemon\n"
        menu_string += "3) Use item\n"
        menu_string += "4) Run away\n"

        return menu_string

    def __get_info_string(self) -> str:
        info_string = ""

        info_string += self.__get_pokemon_info_string(1)
        info_string += "\n"
        info_string += self.__get_pokemon_info_string(2)

        return info_string

    def __get_pokemon_info_string(self, n_pokemon) -> str:
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2
        current_hp = pokemon.base_stats['hp']
        max_hp = pokemon.base_stats['max_hp']

        percentage_hp = int(np.floor((current_hp / max_hp) * 10))

        info_string = "{} - L.{}\n".format(pokemon.name, pokemon.level)
        info_string += "-" * 12 + "\n"
        info_string += "|" + "#" * percentage_hp + " " * (10 - percentage_hp) + "|\t{}/{}\n".format(current_hp, max_hp)
        info_string += "-" * 12 + "\n"

        return info_string

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Submenu

    def __get_moves_menu(self, n_pokemon) -> str:
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2

        moves_string = "The possible moves are:\n"
        for i in range(len(pokemon.moves)):
            move = pokemon.moves[i]
            moves_string += "\t{}) {}/{} - {} - {}\n".format(i + 1, move.pp, move.max_pp, move.name, move.type)

        moves_string += "\n\t0) Return to main menu\n"
        
        return moves_string

