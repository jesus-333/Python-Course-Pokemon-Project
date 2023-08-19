import support
import Trainer

def main():
    trainer_name = input("What is your name?\n")
    
    selected_pokemon = -1
    while selected_pokemon != 1 and selected_pokemon != 2 and selected_pokemon != 3:
        selected_pokemon = input("\nWhat is your starter?\n\t1) Bulbasaur\n\t2) Charmender\n\t3) Squirtle\n")

        if selected_pokemon.isnumeric(): selected_pokemon = int(selected_pokemon)

    starter = support.get_started_pokemon(selected_pokemon)
    trainer = Trainer.Trainer(trainer_name, [starter])
    print(trainer)

    enemy_pokemon = 1 if selected_pokemon + 1 == 4 else selected_pokemon + 1
    enemy = support.get_started_pokemon(enemy_pokemon)

    print("\n\nYour enemy is {}".format(enemy.name))

    selected_move, damage = enemy.use_move(0, trainer.pokemon_list[0])

    print("{} attack you with {}".format(enemy.name, selected_move))
    print("You received {} Hp damage".format(damage))
    
if __name__ == '__main__':
    main()
