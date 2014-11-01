import tornado.web
import tornado.websocket
import tornado.ioloop
import os,sys
from queue import Empty

settings = {
  "static_path": os.path.join(os.path.dirname(__file__),"www"),
  "cookie_secret": "134449a1d4",
  "xsrf_cookies": True
}

clients = []

class IndexHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(request):
    print("rendering request")
    request.render("www/index.html")


class WebSocketMessageHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self, *args):
    global clients
    print("open", "WebSocketChatHandler")
    clients.append(self)

  def on_message(self, message):
    global squeue
    squeue.put(message)     
    print(message)
        
  def on_close(self):
    clients.remove(self)

def check_queue():
  global rqueue
  try:
    event = rqueue.get(False);
    event_category = event.lower().split(':')[0]
    if event == 'QUIT':
      print('OK the webcontrol will quit now')
      tornado.ioloop.IOLoop.instance().stop()
      sys.exit(0)
    elif event_category == 'sfxupdate':
      for c in clients:
        c.write_message(event)
    else:
      print(event)
  except (Empty):
    pass

def startup(recieve_queue, send_queue):
  global rqueue, squeue
  rqueue = recieve_queue
  squeue = send_queue
  app = tornado.web.Application([
  (r'/ws', WebSocketMessageHandler),
  (r'/', IndexHandler),
  (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']))
  ])

  app.listen(80)
  io_loop = tornado.ioloop.IOLoop.instance()
  tornado.ioloop.PeriodicCallback(check_queue, 100, io_loop).start()
  io_loop.start()