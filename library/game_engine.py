class Game():

    def __init__():
        pass

    def create_trainer():
        trainer_name = input("What is your name?\n")
        
        selected_pokemon = -1
        while selected_pokemon != 1 and selected_pokemon != 2 and selected_pokemon != 3:
            selected_pokemon = input("\nWhat is your starter?\n\t1) Bulbasaur\n\t2) Charmender\n\t3) Squirtle\n")

            if selected_pokemon.isnumeric(): selected_pokemon = int(selected_pokemon)

        starter = support.get_started_pokemon(selected_pokemon)
        trainer = Trainer.Trainer(trainer_name, [starter])
        print(trainer)
