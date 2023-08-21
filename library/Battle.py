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
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                if int(selected_action) == 1: # Attack
                    # Move selection for both pokemon
                    selected_move_idx_1 = self.selected_move_manually(1)
                    selected_move_idx_2 = self.selected_move(2, self.use_ai_player_2)

                    outcome = self.execute_both_moves(selected_move_idx_1, selected_move_idx_2)

                    if outcome == 1 : # Our pokemon win
                        if self.count_pokemon_alive(2) > 0: # The opponent has pokemon alive
                            self.change_pokemon(2, -1)
                        else:
                            continue_battle = False
                            exit_status = 1
                    elif outcome == 2: # Opponent has won
                        if self.count_pokemon_alive(1) > 0: # You have  pokemon alive
                            self.change_pokemon(1, -1)
                        else:
                            continue_battle = False
                            exit_status = -1
                    else:
                        continue

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                elif int(selected_action) == 2: # Change pokemon
                    exit_status = self.change_pokemon(1,1)

                    if exit_status == 0: # Pokemon is not changed
                        continue
                    else: # Pokemon is changed

                        if self.use_ai_player_2:
                            # Select a random move for pokemon 2
                            selected_move_idx_2 = np.random.choice(np.arange(len(self.current_pokemon_2.moves)))
                        else:
                            selected_move_idx_2 = self.selected_move_manually(2)

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                elif int(selected_action) == 3: # Use item
                    pass

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
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

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Attack section

    def selected_move_manually(self, n_pokemon : int):
        """
        Method that allow to select a move for a pokemon of a specific trainer
        n_pokemon = 1 for trainer 1 (your character) or 2 (the enemy)
        """

        menu_string = self.__get_moves_menu(n_pokemon)
        continue_selection = True
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2

        while continue_selection:
            if not self.keep_history: support.clear()
            selected_move = input(menu_string)

            if selected_move.isnumeric():
                selected_move = int(selected_move)

                # To obtain a valid index remove 1
                selected_move -= 1

                # Check the input
                # if -1 it means exit otherwise is the index of the move
                if selected_move >= -1 and selected_move < len(pokemon.moves): 
                    continue_selection = False
                else:
                    print("Action not valid")

        return selected_move

    def selected_move(self, n_pokemon : int, random_selection : bool = False) -> int:
        """
        Allow to randomly or manualy select a move for a pokemon.
        Return the index of the selected move.
        """

        if random_selection:
            current_pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2
            selected_move_idx = np.random.choice(np.arange(len(current_pokemon.moves)))
        else:
            selected_move_idx = self.selected_move_manually(n_pokemon)

        return selected_move_idx

    def execute_single_move(self, n_attacker : int, n_defender : int, idx_move : int, random_mode = False):
        """
        Methods when only a pokemon attack. Return 1 if the attacker defeat the defender. Otherwise return 0
        """
        attacker = self.current_pokemon_1 if n_attacker == 1 else self.current_pokemon_2
        defender = self.current_pokemon_1 if n_defender == 1 else self.current_pokemon_2

        damage = attacker.use_move(idx_move, defender)
        if not random_mode: self.__print_move_outcome(damage, attacker, defender, idx_move)

        if damage < 0 : damage = 0
        defender.base_stats['hp'] -= damage

        if defender.base_stats['hp'] <= 0:
            defender.base_stats['hp'] = 0
            return 1
        else:
            return 0

    def execute_both_moves(self, idx_moves_1 : int, idx_moves_2 : int):
        """
        Methods if both pokemon attack in the same turn.
        Return 1 if one of the two pokemon is KO. Otherwise it return 0
        """
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
            first_pokemon.base_stats['hp'] -= damage

            if first_pokemon.base_stats['hp'] <= 0: # Slower pokemon win
                first_pokemon.base_stats['hp'] = 0
                return 1 if second_pokemon.name == self.current_pokemon_1 else 2
        else: # Faster pokemon win
            second_pokemon.base_stats['hp'] = 0
            return 1 if first_pokemon.name == self.current_pokemon_1 else 2
        
        # Nobody win
        return 0

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
    # Change pokemon section

    def change_pokemon(self, n_trainer : int, enter_status : int = 1, random_mode : bool = False) -> int:
        """
        Method to change the current pokemon specified by n_trainer (1 for trainer_1 and 2 for trainer_2)
        Return 1 if the pokemon is changed 0 otherwise
        """
        if random_mode: # Random selection
            while True:
                if n_trainer == 1: 
                    self.current_pokemon_1 = np.random.choice(self.trainer_1.pokemon_list)
                    if self.current_pokemon_1.base_stats['hp'] > 0: return 1
                elif n_trainer == 2:
                    self.current_pokemon_2 = np.random.choice(self.trainer_2.pokemon_list)
                    if self.current_pokemon_2.base_stats['hp'] > 0: return 1
                else:
                    raise ValueError("n_trainer not valid")
        else: # Manually selection
            return self.change_pokemon_manually(n_trainer, enter_status)


    def change_pokemon_manually(self, n_trainer : int, enter_status : int) -> int: 
        """
        Change the pokemon.
        n_trainer = trainer who has to change the pokemon
        enter_status = specify if the pokemon must be changed due to exhaustion (-1) or by choice (1)

        Return 1 if the pokemon is changed otherwise return 0
        """

        trainer = self.trainer_1 if n_trainer == 1 else self.trainer_2

        continue_selection = True

        while continue_selection:
            if not self.keep_history: support.clear()
            select_pokemon = input(self.__get_chagen_pokemon_string(n_trainer))

            if select_pokemon.isnumeric():
                if int(select_pokemon) == 0: # Return to previous menu
                    if enter_status == -1: print("You have to select a new pokemon before return to battle")
                    else: 
                        exit_status = 0
                        continue_selection = False
                elif int(select_pokemon) < 0 or int(select_pokemon) > len(trainer.pokemon_list): # The index is not valid
                    print("Selection not valid")
                else: # Pass a valid index
                    # Note that in the menu the pokemon are numbered from 1
                    new_pokemon = trainer.pokemon_list[int(select_pokemon) - 1]

                    if new_pokemon.base_stats['hp'] <= 0: 
                        print("{} has no hp. Select another pokemon".format(new_pokemon.name))
                    else:
                        if n_trainer == 1:
                            self.current_pokemon_1 = new_pokemon
                        elif n_trainer == 2:
                            self.current_pokemon_2 = new_pokemon
                        else:
                            raise ValueError("Wrong n_trainer")
                         
                        exit_status = 1
                        continue_selection = False

            input("Press Enter to continue...")

        return exit_status



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

    def __get_chagen_pokemon_string(self, n_trainer) -> str:
        trainer = self.trainer_1 if n_trainer == 1 else self.trainer_2
        
        string_team = "Select the pokemon you want:\n"

        for i in range(len(trainer.pokemon_list)):
            pokemon = trainer.pokemon_list[i]
            string_team += "\t{}) {}/{} - {}\n".format(i + 1, pokemon.base_stats['hp'], pokemon.base_stats['max_hp'], pokemon.name)
        
        string_team += "\n\t0) Return to fight\n\n"

        return string_team

    def count_pokemon_alive(self, n_trainer : int) -> int:
        trainer = self.trainer_1 if n_trainer == 1 else self.trainer_2
        count_alive = 0

        for pokemon in trainer.pokemon_list:
            if pokemon.base_stats['hp'] >= 0:
                count_alive += 1

        return count_alive
    
