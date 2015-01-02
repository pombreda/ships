""" Settings for ships """

def GAME_CLASS():
    """ Get the game class """
    from .game import Ships
    return Ships

PLAYER      = 2
# AUTO_UPDATE is usally used during prototyping when where is no SVG renderer
# yet. Later the game will decide if there is a change to update on the clients
# GUI.
AUTO_UPDATE = True
ENCODING    = "UTF-8"
SECRET      = (
    "bOKBlbsEcGa3nHKOuKoVzRMLEU0tD58h"
    "60J5I7oAxqJZJJWySSt0jBJkHLsnJC4E"
    "MxkD0wIbS7Qs0qiDqq4eZMTCqPvxrAp1"
    "ScCK1YlH5dqUsFDKlCoWQbEei06GcRlf"
)
