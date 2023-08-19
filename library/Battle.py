import numpy as np

from . import support, Pokemon

class Battle():
    def __init__(self, trainer_1, trainer_2, use_ai_player_2 = True, keep_history : bool = False):
        self.keep_history = keep_history
        self.use_ai_player_2 = use_ai_player_2

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
                    selected_move_idx_1 = self.selected_move(1)

                    if self.use_ai_player_2:
                        # Select a random move for pokemon 2
                        selected_move_idx_2 = np.random.choice(np.arange(len(self.current_pokemon_2.moves)))
                    else:
                        selected_move_idx_2 = self.selected_move(2)

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

    def selected_move(self, n_pokemon : int):
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

    def execute_moves(self, idx_moves_1 : int, idx_moves_2 : int):
        if self.current_pokemon_1.base_stats['speed'] > self.current_pokemon_2.base_stats['speed']: # Pokemon 1 is faster
            first_pokemon, second_pokemon = self.current_pokemon_1, self.current_pokemon_2
            first_idx, second_idx = idx_moves_1, idx_moves_2
        elif self.current_pokemon_1.base_stats['speed'] < self.current_pokemon_2.base_stats['speed']: # Pokemon 2 is faster
            first_pokemon, second_pokemon = self.current_pokemon_2, self.current_pokemon_1
            first_idx, second_idx = idx_moves_2, idx_moves_1
        else: # Both pokemon have the same speed
            # Select randomly the first
            tmp_list = [(self.current_pokemon_1, idx_moves_1), (self.current_pokemon_2, idx_moves_2)]
            np.random.shuffle(tmp_list)
            first_pokemon, first_idx = tmp_list[0]
            second_pokemon, second_idx = tmp_list[1]
        
        # Compute the damage of the faster pokemon and print the outcome
        damage =  first_pokemon.use_move(first_idx, second_pokemon)
        self.__print_move_outcome(damage, first_pokemon, second_pokemon, first_idx)

        # If the move failed or finish PP the damage is lower than 0 so it is set to 0 for computation
        if damage < 0 : damage = 0
        # Remove damage to hp
        second_pokemon.base_stats['hp'] -= damage

        if second_pokemon.base_stats['hp'] > 0: # The slower pokemon is still alive
            # Same as for the faster pokemon
            damage =  second_pokemon.use_move(second_idx, first_pokemon)
            self.__print_move_outcome(damage, second_pokemon, first_pokemon, second_idx)
            if damage < 0 : damage = 0
            second_pokemon.base_stats['hp'] -= damage

            if first_pokemon.base_stats['hp'] <= 0: # Slower pokemon win
                return 1 if second_pokemon.name == self.current_pokemon_1 else 2
        else: # Faster pokemon win
            return 1 if first_pokemon.name == self.current_pokemon_1 else 2
        
        # Nobody win
        return 0



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
    # Submenu and other stuff

    def __get_moves_menu(self, n_pokemon) -> str:
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2

        moves_string = "The possible moves are:\n"
        for i in range(len(pokemon.moves)):
            move = pokemon.moves[i]
            moves_string += "\t{}) {}/{} - {} - {}\n".format(i + 1, move.pp, move.max_pp, move.name, move.type)

        moves_string += "\n\t0) Return to main menu\n"
        
        return moves_string

    def __print_move_outcome(self, damage, attacker : "Pokemon", defender : "Pokemon", idx_move : int):
        if damage == -1: 
            print("{} miss {} with {}".format(attacker.name, defender.name, attacker.moves[idx_move]))
        elif damage == -2:
            print("{} finished the PP".format(attacker.moves[idx_move]))
        else:
            print("{} use {}".format(attacker.name, attacker.moves[idx_move].name))
            print("{} receive {} damage to hp".format(defender.name, damage))

