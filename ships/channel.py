""" Postgres communication channel """

import psycopg2
import psycopg2.extensions as pext
import tornado.gen as gen
import tornado.ioloop as ioloop
from .sql import db


class Channel(object):
    def __init__(self, game_id, callback):
        self._game_id = game_id
        self._callback = callback
        self._ioloop = ioloop.IOLoop.instance()
        self._conn = psycopg2.connect(db.dsn)
        self._conn.set_isolation_level(
            pext.ISOLATION_LEVEL_AUTOCOMMIT
        )
        self._ioloop.add_handler(
            self._conn.fileno(),
            self._receive,
            self._ioloop.READ
        )
        curs = self._conn.cursor()
        curs.execute("LISTEN %s;" % game_id)

    @property
    def game_id(self):
        return self._game_id

    @gen.coroutine
    def _receive(self, fd, events):
        """ Receive messages from channel """
        state = self._conn.poll()
        if state == pext.POLL_OK:
            if self._conn.notifies:
                notify = self._conn.notifies.pop()
                yield self._callback(notify)
