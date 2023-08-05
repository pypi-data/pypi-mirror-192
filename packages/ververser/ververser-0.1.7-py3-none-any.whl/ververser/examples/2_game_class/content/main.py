from pyglet.gl import glClearColor
import random
from typing import Optional
from ververser import GameWindow


class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window

    def update( self, dt ):
        random_range = 0.1
        r = 0.5 + (( random_range * random.uniform(0, 1) ) - 0.5 * random_range )
        glClearColor( 0, r, 0, 1.0 )

    def draw( self ):
        ...


# --------
# This is just some boilerplate that makes it easier to use a custom Game class

_GAME : Optional[ Game ] = None

def vvs_init( game_window : GameWindow ):
    global _GAME
    _GAME = Game( game_window )

def vvs_update( dt ):
    _GAME.update( dt )

def vvs_draw():
    _GAME.draw()