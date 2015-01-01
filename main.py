""" Main routing for tornado app """

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web


def main():
    """ Initialize tornado IOLoop and webserver """
    handlers = [
        (r'/', tornado.web.StaticFileHandler, {'path': 'static/index.html'}),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
    ]
    application = tornado.web.Application(handlers)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
