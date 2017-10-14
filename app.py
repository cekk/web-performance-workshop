import os
import tornado.ioloop
import tornado.web
from tornado.options import options, define
from tornado.netutil import bind_unix_socket
from tornado.httpserver import HTTPServer

define('unix_socket', default="/tmp/nginx.socket", help='Path to unix socket to bind')
DEBUG = 'DYNO' not in os.environ

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hola, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], debug=DEBUG)

if __name__ == "__main__":
    app = make_app()
    if not DEBUG:
        server = HTTPServer(app)
        socket = bind_unix_socket(options.unix_socket)
        server.add_socket(socket)
        open('/tmp/app-initialized', 'w').close()
    else:
        port = os.environ.get("PORT", '8000')
        app.listen(port)
    tornado.ioloop.IOLoop.current().start()
