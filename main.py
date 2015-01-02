""" Main routing for tornado app """

import os
import momoko
from datetime import datetime
import msgpack
import tornado.httpserver as http
import tornado.ioloop as ioloop
import tornado.web as web
import tornado.gen as gen
import tornado.template as template
import tornado.log as tlog
import ships.websockets as sockets
import logging as lg
import ships.security as sec
import ships.settings as s
from ships.sql import db

tmpl = template.Loader(r'template')

class MainHandler(web.RequestHandler):
    # pylint: disable=too-few-public-methods, abstract-method, star-args
    # pylint: disable=arguments-differ
    """ Main handler for entry page """

    @gen.coroutine
    def get(self, game):
        """ Redirect to index """
        player = yield self.find_player(game)
        host = self.request.host
        data = {
            'game': game,
            'player': str(player),
            'secret': sec.client_verify(game, player)
        }
        if 'DEBUG' in os.environ:
            data['ws_url'] = "ws://%s/main" % host
        else:
            data['ws_url'] = "wss://%s/main" % host
        resp = tmpl.load("game.tmpl").generate(**data)
        self.write(resp)

    @gen.coroutine
    def find_player(self, game):
        """ Finding game / the player id """
        connection = yield momoko.Op(db.getconn)
        with db.manage(connection):
            yield momoko.Op(connection.execute, "BEGIN")
            try:
                cursor = yield momoko.Op(
                    connection.execute,
                    """
                        SELECT
                            players
                        FROM
                            game
                        WHERE
                            game_id = %s
                    """,
                    (game,)
                )
                players = cursor.fetchone()
                if players is None:
                    state = msgpack.dumps({})
                    yield momoko.Op(
                        connection.execute,
                        """
                            INSERT INTO
                                game
                            VALUES
                                (%s, %s, %s, %s)
                        """,
                        (game,1, state, datetime.now())
                    )
                    return 0

                else:
                    player_count = players[0]
                    if player_count < s.PLAYER:
                        yield momoko.Op(
                            connection.execute,
                            """
                                UPDATE
                                    game
                                SET
                                    players = %s,
                                    timestamp = %s
                                WHERE
                                    game_id = %s;
                            """,
                            (
                                player_count + 1,
                                datetime.now(),
                                game
                            )
                        )
                        return player_count
                    return -1
            finally:
                yield momoko.Op(connection.execute, "COMMIT")

def main():
    """ Initialize tornado IOLoop and webserver """
    lgg = lg.getLogger()
    if 'DEBUG' in os.environ:
        lgg.setLevel(lg.DEBUG)
    lgg.handlers[0].setFormatter(tlog.LogFormatter())
    handlers = [
        (r'/game/(\w+)', MainHandler),
        (r'/static/(.*)', web.StaticFileHandler, {'path': 'static'}),
        (r'/main', sockets.MainSocket),
    ]
    application = web.Application(handlers)
    http_server = http.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
