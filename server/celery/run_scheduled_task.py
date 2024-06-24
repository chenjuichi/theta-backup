# run_scheduled_task.py
from tasks import say_hello

if __name__ == "__main__":
    say_hello.delay()