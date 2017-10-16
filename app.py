#!/usr/bin/env python

import os
import tornado.ioloop
import yaml
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.options import options, define
from tornado.netutil import bind_unix_socket
from tornado.httpserver import HTTPServer

define('unix_socket', default="/tmp/nginx.socket", help='Path to unix socket to bind')
DEBUG = 'DYNO' not in os.environ

class MainHandler(RequestHandler):
    def get(self):
        with open('database.yml') as yfile:
            cats = yaml.load(yfile)
        self.render("templates/index.html", cats=cats)

if __name__ == "__main__":
    app = Application(
        [
            (r"/", MainHandler),
            (r"/img/(.*)", StaticFileHandler, {'path': 'img'}),
            (r"/css/(.*)", StaticFileHandler, {'path': 'css'}),
            (r"/js/(.*)", StaticFileHandler, {'path': 'js'}),
            (r"/vendor/(.*)", StaticFileHandler, {'path': 'vendor'}),
        ], debug=DEBUG)
    if not DEBUG:
        server = HTTPServer(app)
        socket = bind_unix_socket(options.unix_socket)
        server.add_socket(socket)
        open('/tmp/app-initialized', 'w').close()
    else:
        port = os.environ.get("PORT", '8000')
        app.listen(port)
    tornado.ioloop.IOLoop.current().start()
