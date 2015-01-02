""" Base game class """

import abc
import tornado.gen as gen
import logging as lg

class BaseGame(object):
    """ Abstract base class for any ships-kind of game """
    def __init__(self, game_id, player_id):
        """ Initialize the game """
        self._game_id = game_id
        self._player_id = player_id

    @property
    def game_id(self):
        """ Get the game id """
        return self._game_id

    @property
    def player_id(self):
        """ Get the player_id """
        return self._player_id

    @abc.abstractmethod
    @gen.coroutine
    def on_command(self, command):
        """ Handle commands from the player """
        lg.fatal("Command not handled: %s", command)
