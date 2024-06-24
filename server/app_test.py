import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, Namespace

# --------------------------

app = Flask(__name__)  # 初始化Flask物件
#socketio = SocketIO(app, cors_allowed_origins="http://192.168.32.50:8080")
CORS(app, supports_credentials=True, cors_allowed_origins='*')
#CORS(app, resources={r'/socket.io/*': {'origins': 'http://192.168.32.50:8080'}})
#socketio = SocketIO(app)
#socketio = SocketIO(app, cors_allowed_origins="*")

#CORS(app)
#CORS(app, origins='http://192.168.32.50:8080')  # 允许来自指定源的请求

# --------------------------

class SendData(Namespace):
  def __init__(self, namespace=None):
      super(SendData, self).__init__(namespace)

  def on_connect(self):
      print("連接成功")

  def on_connecting(self):
      print("正在連接")

  def on_disconnect(self):
      print("斷開連接")

  def on_connect_failed(self):
      print("連接失敗")

  def on_error(self):
      print("錯誤發生，並且無法被其他事件類型所處理")

  def on_reconnect_failed(self):
      print("重連失敗")

  def on_reconnect(self):
      print("成功重連")

  def on_reconnecting(self):
      print("正在重連")

  def on_update_data(self, data):
      # 前端數據上發
      print(data)

  def on_heartbeat(self):
      print(request.sid)

  def send_data(self, data, room):
      while True:
          self.emit(event='acceptData', data=data, room=room)
          time.sleep(10)

if __name__ == '__main__':
    socket_io = SocketIO(app, cors_allowed_origins='*')
    socket_io.on_namespace(SendData('/mysocket', ))
    socket_io.run(app=app, host='0.0.0.0', port=6500)

# --------------------------
'''
@app.route('/')
def index():
    return 'Hello, world!'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

#@socketio.on('message', namespace='/chat')
#def handle_message(message):
#    print('Received message: ' + message)
#    socketio.emit('message', message, namespace='/chat')

# --------------------------

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=6500)
  #socketio.run(app, host='0.0.0.0', port=6500, transport="websocket")
'''