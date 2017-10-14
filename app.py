import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hola, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    port = os.environ.get("PORT", '5000')
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
