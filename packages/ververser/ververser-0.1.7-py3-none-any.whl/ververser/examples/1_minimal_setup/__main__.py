import logging
from pathlib import Path
from ververser import GameWindow


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    game = GameWindow( Path( __file__ ).parent / 'content' )
    game.run()
