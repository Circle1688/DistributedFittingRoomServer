import redis

from plugin_server.config import REDIS_HOST
from plugin_server.generate import generate_process
from .celery import app


# 连接到 Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

@app.task(queue='high_priority')
def high_priority_task(args):
    task_id = high_priority_task.request.id
    result = generate_process(task_id, args)
    redis_client.zrem("high_task_queue", task_id)
    return result

@app.task(queue='low_priority')
def low_priority_task(args):
    task_id = low_priority_task.request.id
    result = generate_process(task_id, args)
    redis_client.zrem("low_task_queue", task_id)
    return result
