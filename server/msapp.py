import socket

import json

import ctypes     # 2022-12-31 add

from flask import Flask, session, jsonify, request
from flask_cors import CORS

# --------------------------

from ajax.getTable import getTable
from ajax.createTable import createTable
from ajax.updateTable import updateTable
from ajax.deleteTable import deleteTable
from ajax.listTable import listTable
from ajax.excelTable import excelTable

# --------------------------

app = Flask(__name__)  # 初始化Flask物件

hostName = socket.gethostname()
local_ip = socket.gethostbyname(hostName)   # get local ip address
print('\n' + 'Lan ip: ' + '\033[46m' + local_ip + '\033[0m')
print('Build:  ' + '\033[42m' + '2023-08-10' + '\033[0m' + '\n')

host_ip = local_ip

ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # prevent the screen saver or sleep.

# --------------------------

app.config['JSON_AS_ASCII'] = False

# --------------------------

app.register_blueprint(getTable)
app.register_blueprint(updateTable)
app.register_blueprint(deleteTable)
app.register_blueprint(createTable)
app.register_blueprint(listTable)
app.register_blueprint(excelTable)

# --------------------------

CORS(app, resources={r'/*': {'origins': '*'}})

# --------------------------

@app.route("/")
def helloWorld():
  print("hello Theata")
  return "Hello..."

# --------------------------

if __name__ == '__main__':
    app.run(host=host_ip, port=6080, debug=True)
