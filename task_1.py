
def main():
    trainer_name = input("What is your name?\n")
    
    selected_pokemon = -1
    while selected_pokemon != 1 and selected_pokemon != 2 and selected_pokemon != 3:
        selected_pokemon = input("\nWhat is your starter?\n\t1) Bulbasaur\n\t2) Charmender\n\t3) Squirtle\n")

        if selected_pokemon.isnumeric(): selected_pokemon = int(selected_pokemon)


if __name__ == '__main__':
    main()
