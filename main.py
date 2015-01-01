""" Main routing for tornado app """

import os
import tornado.httpserver as http
import tornado.ioloop as ioloop
import tornado.web as web


class MainHandler(web.RequestHandler):
    # pylint: disable=too-few-public-methods, abstract-method
    """ Main handler for entry page """
    def get(self):
        """ Redirect to index """
        self.redirect(r'static/index.html')

def main():
    """ Initialize tornado IOLoop and webserver """
    handlers = [
        (r'/', MainHandler),
        (r'/static/(.*)', web.StaticFileHandler, {'path': 'static'}),
    ]
    application = web.Application(handlers)
    http_server = http.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
