""" Websockets for the ships game """

import tornado.websocket as websocket


class MainSocket(websocket.WebSocketHandler):
    # pylint: disable=abstract-method
    """ Main socket, should be the only one, lets see """
    def open(self):
        pass

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        pass
