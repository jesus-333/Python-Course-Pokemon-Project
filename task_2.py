import sys

from library import game_engine

def main(keep_history):
    game = game_engine.Game('data/pokemon_2.json', 'data/moves_2.json', 'data/type_effectiveness_2.json', keep_history)

    game.play_story()

if __name__ == '__main__':
    keep_history = bool( sys.argv[1] )

    main(keep_history)
