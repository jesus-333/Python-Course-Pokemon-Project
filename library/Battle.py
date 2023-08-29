import numpy as np

from . import support, Pokemon

class Battle():
    def __init__(self, trainer_1, trainer_2, use_ai_player_2 = True, keep_history : bool = False, df_effectiveness = None):
        self.keep_history = keep_history
        self.use_ai_player_2 = use_ai_player_2

        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2

        self.current_pokemon_1 = self.trainer_1.pokemon_list[0]
        self.current_pokemon_2 = self.trainer_2.pokemon_list[0]

        if df_effectiveness is not None: self.df_effectiveness = df_effectiveness

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
                    selected_move_idx_1 = self.select_move_manually(1)
                    selected_move_idx_2 = self.select_move(2, self.use_ai_player_2)
                    
                    # Skip the battle if no move was selected
                    if selected_move_idx_1 == -1 : continue

                    # Execute the move and evaluate the outcome
                    outcome, _, _ = self.execute_both_moves(selected_move_idx_1, selected_move_idx_2)
                    exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)
                    
                    # Return the number of the pokemon that win
                    exit_status = exit_status_battle


                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                elif int(selected_action) == 2: # Change pokemon
                    exit_status_change = self.change_pokemon(1, 1, random_mode = False)

                    if exit_status_change == 0: # Pokemon is not changed
                        continue
                    else: # Pokemon is changed

                        # Your opponent attack you after the change
                        selected_move_idx_2 = self.select_move(2, random_mode = self.use_ai_player_2)
                        outcome = self.execute_single_move(2, 1, selected_move_idx_2, print_info = True)
                        exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)
                        
                        # In the case the pokemon go ko after the change
                        exit_status = exit_status_battle

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                elif int(selected_action) == 3: # Use item
                    exit_status_item = self.use_item()

                    if exit_status_item == 0: # No item used
                        continue
                    elif exit_status_item == 1: # Potion used
                        print("You used a potion")
                    elif exit_status_item == 2: # Use a pokeball
                        print("You launch a pokeball...")

                        catch_outcome = self.catch_pokemon()

                        if catch_outcome == 0: # Pokemon escaped
                            print("The {} escape from the pokeball".format(self.current_pokemon_2.name))
                        elif catch_outcome == 1: # Pokemon captured
                            if len(self.trainer_1.pokemon_list) < 6: # You have less than 6 pokemon
                                print("You captured a wild {}".format(self.current_pokemon_2.name))
                                self.trainer_1.pokemon_list.append(self.current_pokemon_2)
                            else:
                                print("You reach the max number of pokemon in the team")
                                print("You free the captured pokemon that run away")

                            continue_battle = False
                            exit_status = 3
                        
                    # This if is valid only if you use a potion or if the opponent escape from the pokeball
                    if continue_battle and exit_status_item != 0:
                        # Your opponent attack you after you used the item
                        selected_move_idx_2 = self.select_move(2, random_mode = self.use_ai_player_2)
                        outcome = self.execute_single_move(2, 1, selected_move_idx_2, print_info = True)
                        exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)
                        
                        # In the case the pokemon go ko after the item is used
                        exit_status = exit_status_battle

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                elif int(selected_action) == 4: # Run away
                    if np.random.rand() <= 0.6:
                        print("\nYou ran away")
                        continue_battle = False
                        exit_status = 4
                        continue
                    else:
                        print("You can't run away")

                        # Your opponent attack you after you fail to escape
                        selected_move_idx_2 = self.select_move(2, random_mode = self.use_ai_player_2)
                        outcome = self.execute_single_move(2, 1, selected_move_idx_2, print_info = True)
                        exit_status_battle, continue_battle = self.eveluate_battle_outcome(outcome)

                else:
                    print("Action not valid")
            else:
                print("Action not valid")

            input("Press Enter to continue...")
            
        print("The battle is over.")
        return exit_status

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Attack section

    def select_move_manually(self, n_pokemon : int):
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

    def select_move(self, n_pokemon : int, random_mode : bool = False) -> int:
        """
        Allow to randomly or manualy select a move for a pokemon.
        Return the index of the selected move.
        """

        if random_mode:
            current_pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2
            selected_move_idx = np.random.choice(np.arange(len(current_pokemon.moves)))
        else:
            selected_move_idx = self.select_move_manually(n_pokemon)

        return selected_move_idx

    def execute_single_move(self, n_attacker : int, n_defender : int, idx_move : int, print_info = False):
        """
        Methods when only a pokemon attack. Return 1 if the attacker defeat the defender. Otherwise return 0
        """
        attacker = self.current_pokemon_1 if n_attacker == 1 else self.current_pokemon_2
        defender = self.current_pokemon_1 if n_defender == 1 else self.current_pokemon_2

        attacker_id = 1 if n_attacker == 1 else 2

        damage = attacker.use_move(idx_move, defender)
        if print_info: self.__print_move_outcome(damage, attacker, defender, idx_move)

        if damage < 0 : damage = 0
        defender.base_stats['hp'] -= damage

        if defender.base_stats['hp'] <= 0:
            defender.base_stats['hp'] = 0
            return attacker_id
        else:
            return 0

    def execute_both_moves(self, idx_moves_1 : int, idx_moves_2 : int, print_var = True):
        """
        Methods if both pokemon attack in the same turn.
        Return 1 if trainer_1 wins, 2 if trainer_2 wins, 0 otherwise 
        """
        if self.current_pokemon_1.base_stats['speed'] > self.current_pokemon_2.base_stats['speed']: # Pokemon 1 is faster
            first_pokemon, second_pokemon = self.current_pokemon_1, self.current_pokemon_2
            first_idx, second_idx = idx_moves_1, idx_moves_2
            first_identifier, second_identifier = 1, 2 # Used to return the winner
        elif self.current_pokemon_1.base_stats['speed'] < self.current_pokemon_2.base_stats['speed']: # Pokemon 2 is faster
            first_pokemon, second_pokemon = self.current_pokemon_2, self.current_pokemon_1
            first_idx, second_idx = idx_moves_2, idx_moves_1
            first_identifier, second_identifier = 2, 1 # Used to return the winner
        else: # Both pokemon have the same speed
            # Select randomly the first
            tmp_list = [(self.current_pokemon_1, idx_moves_1, 1), (self.current_pokemon_2, idx_moves_2, 2)]
            np.random.shuffle(tmp_list)
            first_pokemon, first_idx, first_identifier = tmp_list[0]
            second_pokemon, second_idx, second_identifier = tmp_list[1]
        
        # Compute the damage of the faster pokemon and print the outcome
        effect = self.compute_effectiveness(first_pokemon, second_pokemon)
        damage_first =  first_pokemon.use_move(first_idx, second_pokemon, effect)
        if print_var: self.__print_move_outcome(damage_first, first_pokemon, second_pokemon, first_idx)

        # If the move failed or finish PP the damage is lower than 0 so it is set to 0 for computation
        if damage_first < 0 : damage_first = 0
        # Remove damage to hp
        second_pokemon.base_stats['hp'] -= damage_first

        if second_pokemon.base_stats['hp'] > 0: # The slower pokemon is still alive
            # Same as for the faster pokemon
            effect = self.compute_effectiveness(second_pokemon, first_pokemon)
            damage_second =  second_pokemon.use_move(second_idx, first_pokemon, effect)
            if print_var: self.__print_move_outcome(damage_second, second_pokemon, first_pokemon, second_idx)
            if damage_second < 0 : damage_second = 0
            first_pokemon.base_stats['hp'] -= damage_second

            if first_pokemon.base_stats['hp'] <= 0: # Slower pokemon win
                first_pokemon.base_stats['hp'] = 0
                return second_identifier, (damage_first, first_identifier), (damage_second, second_identifier)
        else: # Faster pokemon win
            second_pokemon.base_stats['hp'] = 0
            return first_identifier,(damage_first, first_identifier), (damage_second, second_identifier) 
        
        # Nobody win
        return 0, (damage_first, first_identifier), (damage_second, second_identifier)

    def compute_effectiveness(self, attacker : "Pokemon", defender : "Pokemon") -> float :
        effect = 1
        for attacker_type in attacker.types:
            for defender_type in defender.types:
                if attacker_type == 'fairy' or attacker_type == 'steel' or defender_type == 'fairy' or defender_type == 'steel':
                    # steel and fairy type not present in the effectiveness file
                    effect = 1
                else:
                    attacker_filter = (self.df_effectiveness['attack'] == attacker_type)
                    defender_filter = (self.df_effectiveness['defend'] == defender_type)
                    
                    effect *= float(self.df_effectiveness[np.logical_and(attacker_filter, defender_filter)]['effectiveness'])
                    # effect *= float(self.df_effectiveness[attacker_filter & defender_filter]['effectiveness'])

        return effect

    def eveluate_battle_outcome(self, outcome : int) -> [int, bool]:
        """
        Evaluate the outcome of a battle.
        Return:
            -) exit_status, an integer that determin the outcome of the battle (1 -> trainer_1 wins, 2 -> trainer_2 wins, 0 no one wins)
            -) continue_battle, a bool to indicate if the battle is ended
        """
        continue_battle = True
        exit_status = 0

        if outcome == 1 : # Our pokemon win
            if self.count_pokemon_alive(2) > 0: # The opponent has pokemon alive
                self.change_pokemon(2, -1, random_mode = False)
            else: # No pokemon alive for the opponent
                continue_battle = False
                exit_status = 1
        elif outcome == 2: # Opponent has won
            if self.count_pokemon_alive(1) > 0: # You have  pokemon alive
                self.change_pokemon(1, -1, random_mode = self.use_ai_player_2)
            else: # No pokemon alive for the protagonist
                continue_battle = False
                exit_status = 2

        return exit_status, continue_battle

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
            select_pokemon = input(self.__get_change_pokemon_string(n_trainer))

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

        return exit_status

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
    # Use item section

    def use_item(self) -> int:
        """
        Method to use a item. Valid only for trainer 1 (the protagonist)
        Return an int called exit_status:
            0 = No object used
            1 = Potion used
            2 = Pokeball used
        """
        continue_selection = True
        exit_status = -1

        while continue_selection:
            if not self.keep_history: support.clear()

            item_selection = input(self.__get_item_menu(1))

            if item_selection.isnumeric():
                if int(item_selection) == 0: # No object
                    continue_selection = False
                    exit_status = 0
                elif int(item_selection) == 1: # Potion
                    if self.trainer_1.potion > 0:
                        self.trainer_1.potion -= 1
                        self.current_pokemon_1.base_stats['hp'] += 20
                        
                        # Reset the hp to the maximum
                        if self.current_pokemon_1.base_stats['hp'] > self.current_pokemon_1.base_stats['max_hp']:
                            self.current_pokemon_1.base_stats['hp'] = self.current_pokemon_1.base_stats['max_hp']

                        continue_selection = False
                        exit_status = 1
                    else:
                        print("You finish the potion")

                elif int(item_selection) == 2: # Pokeball
                    if self.trainer_1.pokeball > 0:
                        self.trainer_1.pokeball -= 1
                        continue_selection = False
                        exit_status = 2
                    else:
                        print("You finish the pokeball")
                else:
                    print("Selection not valid")
            else:
                print("Selection not valid")

        return exit_status

    def catch_pokemon(self) -> int:
        """
        Method used to catch the opponent pokemon.
        Return 1 if the pokemon is captured or 0 otherwise
        """
        
        catch_probability = 1 - (self.current_pokemon_2.base_stats['hp'] / self.current_pokemon_2.base_stats['max_hp'])
        
        if np.random.rand() <= catch_probability:
            return 1
        else: 
            return 0
        

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Main battle menu

    def __get_main_menu_string(self) -> str:
        menu_string = ""
        menu_string += "1) Attack\n"
        menu_string += "2) Change Pokemon\n"
        menu_string += "3) Use item\n"
        menu_string += "4) Run away\n\n"

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

        bar_length = 20
        percentage_hp = int(np.floor((current_hp / max_hp) * bar_length))

        info_string = "{} - L.{}\n".format(pokemon.name, pokemon.level)
        info_string += "-" * (bar_length + 2) + "\n"
        info_string += "|" + "#" * percentage_hp + " " * (bar_length - percentage_hp) + "|\t{}/{}\n".format(current_hp, max_hp)
        info_string += "-" * (bar_length + 2) + "\n"

        return info_string

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Submenu and other stuff

    def __get_moves_menu(self, n_pokemon) -> str:
        pokemon = self.current_pokemon_1 if n_pokemon == 1 else self.current_pokemon_2

        moves_string = "The possible moves are:\n"
        for i in range(len(pokemon.moves)):
            move = pokemon.moves[i]
            moves_string += "\t{}) {}/{} - {} - {}\n".format(i + 1, move.pp, move.max_pp, move.name, move.type)

        moves_string += "\n\t0) Return to main menu\n\n"
        
        return moves_string

    def __get_item_menu(self, n_trainer : int) -> str:
        trainer = self.trainer_1 if n_trainer == 1 else self.trainer_2
        
        item_string = "Your items are:\n"

        item_string += "\t1) Potion   : {}/10\n".format(trainer.potion)
        item_string += "\t2) Pokeball : {}/10\n\n".format(trainer.pokeball)
        item_string += "\t0) Exit\n\n"

        return item_string

    def __print_move_outcome(self, damage, attacker : "Pokemon", defender : "Pokemon", idx_move : int):
        if damage == -1: 
            print("{} miss {} with {}".format(attacker.name, defender.name, attacker.moves[idx_move]))
        elif damage == -2:
            print("{} finished the PP".format(attacker.moves[idx_move]))
        else:
            print("{} use {}".format(attacker.name, attacker.moves[idx_move].name))
            print("{} receive {} damage to hp".format(defender.name, damage))

    def __get_change_pokemon_string(self, n_trainer) -> str:
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
            if pokemon.base_stats['hp'] > 0:
                count_alive += 1

        return count_alive
    
