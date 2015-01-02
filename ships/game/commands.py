""" Commands of the game ships """

import freeze
import os

def set(state, *args):
    """ Test command: set a value """
    state['val'] = args[0]
    return "value set"

def get(state):
    """ Test command: get a value """
    return state['val']
