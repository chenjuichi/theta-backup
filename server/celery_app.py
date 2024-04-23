import os
import time
import socket

# --------------------------

from tasks import process_excel_file
from celery import Celery
from celery.schedules import crontab

import redis
from redis.exceptions import ConnectionError

from datetime import timedelta
import glob

# --------------------------

#hostName = socket.gethostname()
#local_ip = socket.gethostbyname(hostName)   # get local ip address
#print('\n' + 'Lan ip: ' + '\033[46m' + local_ip + '\033[0m')
#print('Build:  ' + '\033[42m' + '2023-08-10' + '\033[0m' + '\n')
#host_ip = local_ip

# --------------------------

app = Celery(__name__)
# 使用 Redis 作為 broker 和 result backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# 新增這個設置
app.conf.broker_connection_retry_on_startup = True

# 使用新的配置名稱
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = 'Asia/Taipei'

# --------------------------

# 檢查 Redis 連接是否可用的函數
def check_redis_server():
  try:
    #connection = redis.StrictRedis.from_url(redis_url)
    connection = redis.StrictRedis()
    connection.ping()
    return True
  except ConnectionError:
    return False

# --------------------------

# Define the Celery task
@app.task
def process_files_in_directory(directory, pattern):
    try:
      matching_files = glob.glob(f"{directory}/{pattern}")
      for file_path in matching_files:
        result =  process_excel_file.apply_async(args=[file_path], kwargs={'pattern': os.path.basename(file_path)})

        # 檢查是否成功放置任務
        if result.successful():
          #task_id = result.id
          task_id = result.get(timeout=2)
          print(f"Task ID: {task_id}")
    except Exception as e:
        # Handle the exception, log it, or take corrective actions
        print(f"An error occurred: {e}")

# --------------------------

# Schedule the task to run every day at 9:00 AM and 2:00 PM
base_directory = 'c:\\theata'
pattern = 'Report_*.xlsx'
schedule_args = [(base_directory, pattern)]
matching_files = glob.glob(f"{base_directory}/{pattern}")
schedule_args = [(schedule_args[0][0], os.path.basename(file)) for file in matching_files]
#print("schedule_args: ", schedule_args)

beat_schedule = {}
for idx, args in enumerate(schedule_args):
  #print("args: ", args)
  beat_schedule[f'process-task-{idx}'] = {
    'task': 'celery_app.process_files_in_directory',
    #'schedule': timedelta(hours=10, minutes=50)  if idx % 2 == 0 else timedelta(hours=14, minutes=0) ,
    'schedule': crontab(hour=15, minute=12) if idx % 2 == 0 else crontab(hour=16, minute=0),
    'args': args,
    #'options': {
    #  'name': 'scan_files_morning' if idx % 2 == 0 else 'scan_files_afternoon',
    #},
    #'options': {
    #  'name': f'scan_files_{idx}',
    #},
  }

#print("beat_schedule: ", beat_schedule)
app.conf.beat_schedule = beat_schedule

# --------------------------
'''
if __name__ == '__main__':
  try:
    # Check if Redis server is running
    if not check_redis_server():
      print("Redis server is not running. Please start Redis server.")
    else:
      # Check Redis connection
      #while not check_redis_connection():
      #  print("Waiting for Redis connection...")
      #  time.sleep(2)

      # Start Celery Worker
      celery.worker_main(['celery', '-A', 'app.celery', 'worker', '--loglevel=info'])
  except KeyboardInterrupt:
      print("Celery Worker terminated by user.")

  try:
    # Start Celery Beat
    celery.conf.CELERYBEAT_SCHEDULE = beat_schedule
    celery.beat_main(['celery', '-A', 'app.celery', 'beat', '--loglevel=info'])
    #celery.Beat().run_scheduler(app=celery)
  except KeyboardInterrupt:
    print("Celery Beat terminated by user.")

  try:
    # Start Flask Application
    app.run(host=local_ip, port=6080, debug=True)
  except KeyboardInterrupt:
    print("Flask Application terminated by user.")

  if check_redis_server():
    # Start Celery Worker
    celery.worker_main(['celery', '-A', 'app.celery', 'worker', '--loglevel=info'])

    # Start Celery Beat
    celery.conf.CELERYBEAT_SCHEDULE = beat_schedule
    celery.beat_main(['celery', '-A', 'app.celery', 'beat', '--loglevel=info'])

    # Start Flask Application
    app.run(host=local_ip, port=6080, debug=True)
  else:
    print("Error: Redis is not available. Please make sure Redis is running.")
'''
