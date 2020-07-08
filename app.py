import tornado.ioloop
import tornado.web

import redis
import socket

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.database = redis.Redis(host='localhost', port=6379, db=0)

        if(self.database.get('counter') == None):
            self.database.set("counter", 0)

        visitCount = int(self.database.get('counter'))
        visitCount = visitCount + 1
        hostName = socket.gethostname()
        ipAddr = socket.gethostbyname(hostName)
        self.database.set("counter", visitCount)
        self.write("Hello! This page is visited %d time(s)<br>current recorded IP is %s" % (visitCount, ipAddr))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()