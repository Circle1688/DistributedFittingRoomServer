from celery import Celery
from kombu import Queue, Exchange
from plugin_server.config import REDIS_HOST

# app = Celery('faceswap',
#              broker=f'redis://{REDIS_HOST}',
#              backend=f'redis://{REDIS_HOST}',
#              include=['faceswap.tasks'])

# # 配置队列
# app.conf.task_queues = (
#     Queue('high_priority', routing_key='high_priority'),
#     Queue('low_priority', routing_key='low_priority'),
# )
#
# # 默认队列
# app.conf.task_default_queue = 'high_priority'
# app.conf.task_default_exchange = 'tasks'
# app.conf.task_default_routing_key = 'high_priority'
#
# # 路由规则
# app.conf.task_routes = {
#     'high_priority_task': {'queue': 'high_priority', 'routing_key': 'high_priority'},
#     'low_priority_task': {'queue': 'low_priority', 'routing_key': 'low_priority'},
# }

app = Celery('faceswap', include=['faceswap.tasks'])
CONFIG = {
    # 'CELERY_ACKS_LATE': True, # 亲测不影响。
    'CELERYD_PREFETCH_MULTIPLIER': 1,  # 对于预取的，顺序无法变更，所以设置数量为1.注意0代表不限制
    # 设置时区
    'CELERY_TIMEZONE': 'Asia/Shanghai',
    # 默认为true，UTC时区
    'CELERY_ENABLE_UTC': True,
    # broker
    'BROKER_URL': f'redis://{REDIS_HOST}',
    # backend配置，注意指定redis数据库
    'CELERY_RESULT_BACKEND': f'redis://{REDIS_HOST}',
    # worker最大并发数
    'CELERYD_CONCURRENCY': 1,
    # 如果不设置，默认是celery队列，此处使用默认的直连交换机，routing_key完全一致才会调度到celery_demo队列
    # 此处注意，元组中只有一个值的话，需要最后加逗号
    'CELERY_QUEUES': (
        Queue("facefusion_queue", Exchange("facefusion_queue"), routing_key="facefusion_queue", priority=3),
    )
}

app.config_from_object(CONFIG)

app.conf.update(
    result_expires=3600,
    task_track_started=True,  # 启用任务开始状态跟踪
)

if __name__ == '__main__':
    app.start()
