from library import game_engine

def main():
    game = game_engine.Game('data/pokemon_2.json', 'data/moves_2.json')

    game.play()

if __name__ == '__main__':
    main()
