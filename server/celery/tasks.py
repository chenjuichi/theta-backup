
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/1',
)

app.conf.broker_connection_retry_on_startup = True
app.conf.task_track_started = True
app.conf.task_ignore_result = False
app.conf.timezone = 'Asia/Taipei'

@app.task()
def say_hello():
    print('Hello')

#@app.task()
#def say_hello(parameter):
#    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    print(f'{current_time} - Hello! Parameter: {parameter}')

#if __name__ == '__main__':
#  #multiprocessing.set_start_method('spawn', True)
#  app.worker_main(argv=['worker', '--pool=solo', '-E', '--loglevel=info'])


if __name__ == '__main__':
    app.worker_main(argv=['worker', '--pool=solo', '--loglevel=info', '--without-gossip', '--without-mingle'])
