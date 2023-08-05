from pyglet.gl import glClearColor
import random
from ververser import GameWindow


class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window

    def update( self, dt ):
        random_range = 0.1
        r = 0.5 + (( random_range * random.uniform(0, 1) ) - 0.5 * random_range )
        glClearColor( r, r, 0, 1.0 )

    def draw( self ):
        ...
