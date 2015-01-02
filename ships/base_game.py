""" Base game class """

import logging as lg
from datetime import datetime
import abc
import msgpack
import momoko
import tornado.gen as gen
from . import settings as s
from .sql import db

class BaseGame(object):
    # pylint: disable=abstract-class-not-used
    """ Abstract base class for any ships-kind of game """
    def __init__(self, socket):
        """ Initialize the game """
        self._socket = socket
        self._game_id = socket.game_id
        self._player_id = socket.player_id

    @property
    def socket(self):
        """ Get the socket

        :rtype: ships.websockets.GameSocket
        """
        return self._socket

    @property
    def game_id(self):
        """ Get the game id """
        return self._game_id

    @property
    def player_id(self):
        """ Get the player_id """
        return self._player_id

    @gen.coroutine
    def _on_recv(self, call, data):
        """ Receives messages, loads state, calls game, saves state """
        connection = yield momoko.Op(db.getconn)
        with db.manage(connection):
            yield momoko.Op(connection.execute, "BEGIN")
            try:
                cursor = yield momoko.Op(
                    connection.execute,
                    """
                        SELECT
                            state
                        FROM
                            game
                        WHERE
                            game_id = %s
                    """,
                    (self.game_id,)
                )
                state = cursor.fetchone()[0]
                state = msgpack.loads(state, encoding=s.ENCODING)
                yield call(data, state)
                state = msgpack.dumps(state)
                yield momoko.Op(
                    connection.execute,
                    """
                        UPDATE
                            game
                        SET
                            state = %s,
                            timestamp = %s
                        WHERE
                            game_id = %s;
                    """,
                    (
                        state,
                        datetime.now(),
                        self.game_id
                    )
                )
            finally:
                yield momoko.Op(connection.execute, "COMMIT")

    @abc.abstractmethod
    @gen.coroutine
    def on_command(self, command, state):
        """ Handle commands from the player """
        lg.fatal("Command not handled: %s", command)

    @abc.abstractmethod
    @gen.coroutine
    def on_notify(self, notify, state):
        """ Handle messages from other players """
        lg.fatal("Message not handled: %s", notify)
