""" Websockets for the ships game """

import tornado.websocket as websocket
import tornado.gen as gen
import logging as lg
import json
from . import security as sec

class JsonSocket(websocket.WebSocketHandler):
    # pylint: disable=too-few-public-methods,abstract-method
    """ Adds send_msg which will encode the message as JSON """
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

class MainSocket(JsonSocket):
    # pylint: disable=abstract-method
    """ Main socket, should be the only one, lets see """
    def open(self):
        pass

    @gen.coroutine
    def on_message(self, message):
        lg.debug("Main socket message: %s ", message)
        msg = json.loads(message, encoding="UTF-8")
        if msg['type'] == "ping":
            self.send_msg({'type' : 'pong'})
        elif msg['type'] == "hello":
            verify = sec.client_verify(
                msg['game'],
                msg['player']
            )
            if verify == msg['secret']:
                if int(msg['player']) == -1:
                    self.send_html(0, 'Game is full')
                else:
                    self.send_html(0, 'Welcome: waiting for players')
            else:
                self.send_html(0, 'Access denied')

    def on_close(self):
        pass
