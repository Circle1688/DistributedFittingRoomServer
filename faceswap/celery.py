from celery import Celery
from kombu import Queue, Exchange
from plugin_server.config import REDIS_HOST


app = Celery('faceswap', include=['faceswap.tasks'])
CONFIG = {
    'CELERY_ACKS_LATE': True,
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
    # 如果不设置，默认是celery队列，此处使用默认的直连交换机，routing_key完全一致才会调度到facefusion_queue队列
    'CELERY_QUEUES': (
        Queue("facefusion_queue", Exchange("facefusion_queue"), routing_key="facefusion_queue"),
    )
}

app.config_from_object(CONFIG)

app.conf.update(
    result_expires=3600,
    task_track_started=True,  # 启用任务开始状态跟踪
)

# 开启任务优先级
app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}

if __name__ == '__main__':
    app.start()
