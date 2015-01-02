""" Websockets for the ships game """

import logging as lg
import tornado.websocket as websocket
import tornado.gen as gen
import psycopg2
import json
import msgpack
from . import security as sec
from .channel import Channel
from . import settings as s
from .sql import db

class GameSocket(websocket.WebSocketHandler):
    """ Adds send_* methods for game interaction """
    # pylint: disable=too-few-public-methods,abstract-method
    def __init__(self, application, request, **kwargs):
        self._game_id   = None
        self._player_id = None
        self._game_obj  = None
        self._channel   = None
        super().__init__(application, request, **kwargs)

    def send_msg(self, msg):
        """ Encode JSON """
        message = json.dumps(msg)
        self.write_message(message)

    def send_alert(self, text):
        """ Send a alert to the client """
        self.send_msg({
            'type': 'alert',
            'text': text,
        })

    def send_html(self, display, html):
        """ Send html to the client """
        self.send_msg({
            'type': 'display%d' % display,
            'html': html,
        })

    def send_notify(self, notify):
        """ Send notify to all players """
        notify['sender'] = self._player_id
        lg.debug("Notify sent: %s %s", self._game_id, notify)
        data = json.dumps(notify)
        db.execute(
            "NOTIFY %s, %%s;" % self._game_id,
            (data,),
            callback=self._notify_done
        )

    def _notify_done(self, cursor, error):
        """ Giving feedback """
        lg.debug("Notify callback: %s ", error)
        try:
            lg.debug("%s", cursor.fetchall())
        except psycopg2.ProgrammingError:
            pass

    @property
    def game_id(self):
        """ Return game id """
        return self._game_id

    @property
    def player_id(self):
        """ Return player id """
        return self._player_id


class MainSocket(GameSocket):
    # pylint: disable=abstract-method
    """ Main socket, should be the only class, lets see """
    def open(self):
        pass

    @gen.coroutine
    def on_notify(self, data):
        """ Receives notification from channel and send them to the game """
        msg = json.loads(data, encoding=s.ENCODING)
        lg.debug("Notify received: %s", msg)
        if int(msg['sender']) == self._player_id:
            return
        type_ = msg['type']
        if type_ == 'game_ready':
            self.send_html(0, 'Welcome: ready')
            return
        # pylint: disable=protected-access
        self._game_obj._on_recv(
            self._game_obj.on_notify,
            msg,
        )

    @gen.coroutine
    def on_message(self, message):
        msg = json.loads(message, encoding="UTF-8")
        type_ = msg['type']
        if type_ != "ping":
            lg.debug("Main socket message: %s ", message)
        if type_ == "ping":
            self.send_msg({'type' : 'pong'})
        elif type_ == "hello":
            verify = sec.client_verify(
                msg['game'],
                msg['player']
            )
            if verify == msg['secret']:
                self._game_id = msg['game']
                self._player_id = int(msg['player'])
                if int(self._player_id) == -1:
                    self.send_html(0, 'Game is full')
                else:
                    self._game_obj = s.GAME_CLASS()(self)
                    self._channel = Channel(self.game_id, self.on_notify)
                    if int(self._player_id) + 1 == s.PLAYER:
                        self.send_notify({
                            'type': 'game_ready'
                        })
                        self.send_html(0, 'Welcome: ready')
                    else:
                        self.send_html(0, 'Welcome: waiting for players')
            else:
                self.send_html(0, 'Access denied')
        elif type_ == "command":
            # pylint: disable=protected-access
            self._game_obj._on_recv(
                self._game_obj.on_command,
                msg,
            )

    def on_close(self):
        pass
