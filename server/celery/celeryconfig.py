from tasks import say_hello

from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Taipei'
# 指定 Django 数据库调度器
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'say-hello-morning': {
        'task': 'tasks.say_hello',
        'schedule': crontab(hour=15, minute=59),
    },
    'say-hello-afternoon': {
        'task': 'tasks.say_hello',
        'schedule': crontab(hour=15, minute=58),
    },
}
