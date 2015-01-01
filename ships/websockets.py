""" Websockets for the ships game """

import tornado.websocket as websocket
import logging as lg
import json

class JsonSocket(websocket.WebSocketHandler):
    # pylint: disable=too-few-public-methods,abstract-method
    """ Adds send_msg which will encode the message as JSON """
    def send_msg(self, msg):
        """ Encode JSON """
        message = json.dumps(msg)
        self.write_message(message)

class MainSocket(JsonSocket):
    # pylint: disable=abstract-method
    """ Main socket, should be the only one, lets see """
    def open(self):
        self.send_msg({
            'type': 'alert',
            'text': 'welcome',
        })

    def on_message(self, message):
        lg.debug("Main socket message: %s ", message)
        msg = json.loads(message)
        if msg['type'] == "ping":
            self.send_msg({'type' : 'pong'})

    def on_close(self):
        pass
