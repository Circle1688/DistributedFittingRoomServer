配置Celery

首先安装redis



```
pip install celery
```

```
pip install redis
```



只有在windows系统上需要安装这个，用于启动

```
pip install gevent
```



worker启动命令

```
celery -A faceswap worker -P gevent -Q high_priority,low_priority -l INFO --concurrency=1
```



安装flower监控

```
pip install flower
```



启动监控

```
celery -A faceswap flower
```

