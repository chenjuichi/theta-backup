from celery.result import AsyncResult
from celery_app import app

# 舉例假設您知道任務的 task_id，您可以使用這個 ID 來獲取結果
task_id = 'f2bc8cee-4108-4c95-b25c-920e65e665bd'  # 替換成實際的 task_id

result = AsyncResult(task_id, app=app)

# 檢查任務是否已經完成
if result.ready():
    # 獲取任務的結果
    result_value = result.result
    print(f'Task result: {result_value}')
else:
    print('Task is still pending or in progress.')