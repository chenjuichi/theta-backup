import socket
import json
import ctypes

from flask import Flask, session, jsonify, request
from flask_cors import CORS

# --------------------------

from ajax.getTable import getTable
from ajax.createTable import createTable
from ajax.updateTable import updateTable
from ajax.deleteTable import deleteTable
from ajax.listTable import listTable
from ajax.excelTable import excelTable

from ajax.scheduleDoTable import scheduleDoTable, do_read_all_excel_files, file_ok

import openpyxl

from ajax.scheduleDoTable import scheduleDoTable
from apscheduler.schedulers.background import BackgroundScheduler

# --------------------------

app = Flask(__name__)  # 初始化Flask物件
#cleanup_executed = False

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
app.register_blueprint(scheduleDoTable)

# --------------------------

CORS(app, resources={r'/*': {'origins': '*'}})

with open('database/theta-dataForTheta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

_base_dir = data[0]['baseDir']
_customer_row = data[0]['customer_row']
_spindle_cat_row = data[0]['spindle_cat_row']
_id_row = data[0]['id_row']
_id_column = data[0]['id_column']
_emp_id_row = data[0]['emp_id_row']
_date_row = data[0]['date_row']
_date_column = data[0]['date_column']
_runin_row = data[0]['runin_row']

app.config['baseDir'] = data[0]['baseDir']
app.config['customer_row'] = data[0]['customer_row']
app.config['spindle_cat_row'] = data[0]['spindle_cat_row']
app.config['id_row'] = data[0]['id_row']
app.config['id_column'] = data[0]['id_column']
app.config['emp_id_row'] = data[0]['emp_id_row']
app.config['date_row'] = data[0]['date_row']
app.config['date_column'] = data[0]['date_column']
app.config['runin_row'] = data[0]['runin_row']

f.close()

# --------------------------

# 初始化调度器
scheduler = BackgroundScheduler()

@app.route("/")
def helloWorld():
  print("hello Theata")
  return "Hello..."


@app.route('/hello', methods=['GET'])
def hello():
    print("fetch hello....")
    output = {"name": ""}
    return jsonify(output)

# --------------------------

def my_job1():
    print("hello, Scheduled job1 is running...")
    with app.app_context():
        do_read_all_excel_files()

def my_job2():
    print("hello, Scheduled job2 is running...")
    with app.app_context():
        do_read_all_excel_files()

# 注册第一個作業，每天的 9:00 执行
scheduler.add_job(my_job1, 'cron', hour=9, minute=0)
# 注册第二個作業，每天的 14:00 执行
scheduler.add_job(my_job2, 'cron', hour=14, minute=0)

# --------------------------

if __name__ == '__main__':
  scheduler.start()
  print("Scheduled version...")
  app.run(host=host_ip, port=6080, debug=True)
