""" Postgres communication channel """

from .sql import db

class Channel(object):
    def __init__(self, game):
        self.game = game
