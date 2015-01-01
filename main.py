""" Main routing for tornado app """

import os
import tornado.httpserver as http
import tornado.ioloop as ioloop
import tornado.web as web
import tornado.template as template
import ships.websockets as sockets
import logging as lg
import os

tmpl = template.Loader(r'template')

class MainHandler(web.RequestHandler):
    # pylint: disable=too-few-public-methods, abstract-method, star-args
    """ Main handler for entry page """
    def get(self):
        """ Redirect to index """
        host = self.request.host
        if 'DEBUG' in os.environ:
            data = {
                'ws_url': "ws://%s/main" % host,
            }
        else:
            data = {
                'ws_url': "ws://%s/main" % host,
            }
        resp = tmpl.load("index.html").generate(**data)
        self.write(resp)

def main():
    """ Initialize tornado IOLoop and webserver """
    if 'DEBUG' in os.environ:
        lg.getLogger().setLevel(lg.DEBUG)
    handlers = [
        (r'/', MainHandler),
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
