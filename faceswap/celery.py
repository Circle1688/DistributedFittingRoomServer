from celery import Celery
from kombu import Queue
from plugin_server.config import REDIS_HOST

app = Celery('faceswap',
             broker=f'redis://{REDIS_HOST}',
             backend=f'redis://{REDIS_HOST}',
             include=['faceswap.tasks'])

# 配置队列
app.conf.task_queues = (
    Queue('high_priority', routing_key='high_priority'),
    Queue('low_priority', routing_key='low_priority'),
)

# 默认队列
app.conf.task_default_queue = 'high_priority'
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_routing_key = 'high_priority'

# 路由规则
app.conf.task_routes = {
    'high_priority_task': {'queue': 'high_priority', 'routing_key': 'high_priority'},
    'low_priority_task': {'queue': 'low_priority', 'routing_key': 'low_priority'},
}
app.conf.update(
    result_expires=3600,
    task_track_started=True,  # 启用任务开始状态跟踪
)

if __name__ == '__main__':
    app.start()
