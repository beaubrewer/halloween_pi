import tornado.ioloop
import tornado.web
import tornado.websocket
import os

clients = []
settings = {
  "static_path": os.path.join(os.path.dirname(__file__),"www"),
  "cookie_secret": "134449a1d4",
  "xsrf_cookies": True
}


class IndexHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(request):
    print("rendering request")
    request.render("www/index.html")

class WebSocketChatHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self, *args):
    print("open", "WebSocketChatHandler")
    clients.append(self)

  def on_message(self, message):        
    print(message)
    for client in clients:
        client.write_message(message)
        
  def on_close(self):
    clients.remove(self)

app = tornado.web.Application([
  (r'/ws', WebSocketChatHandler),
  (r'/', IndexHandler),
  (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']))
])

app.listen(8000)
tornado.ioloop.IOLoop.instance().start()