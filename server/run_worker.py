
from celery import Celery
from tasks import say_hello

from celery.result import AsyncResult

app = Celery(
  'tasks',
  broker='redis://localhost:6379/0',
  backend='redis://localhost:6379/1'
)

app.config_from_object('celeryconfig')

result = say_hello.delay()
task_id = result.id
task_result = AsyncResult(task_id)
print(task_result.status)

#print(f'Task ID: {result.id}')
#print(f'Task State: {result.state}')

if __name__ == '__main__':
##   #multiprocessing.set_start_method('spawn', True)
  app.Beat(argv=['beat', '--scheduler', '--loglevel=info', 'django_celery_beat.schedulers:DatabaseScheduler'])
  #app.Beat(argv=['beat', 'django_celery_beat.schedulers:DatabaseScheduler'])

## 启动 Celery Beat 进程
#app.Beat(argv=['beat', '--scheduler', 'django_celery_beat.schedulers:DatabaseScheduler'])
#
'''
## 为了在运行时显示定时任务的效果，可以添加一个无限循环
while True:
  result = say_hello.delay()
  task_id = result.id
  task_result = AsyncResult(task_id)
  if (task_result.status.strip() != 'PENDING'):
    print(task_result.status)
'''