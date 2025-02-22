import time
from fastapi import APIRouter, Depends, HTTPException
from plugin_server.schemas import *
from plugin_server.auth import get_current_user_id
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session

# from faceswap.tasks import high_priority_task, low_priority_task, redis_client
from faceswap.tasks import generate_task, redis_client
from celery.result import AsyncResult

from plugin_server.task_routes import add_task

router = APIRouter()


def create_generate_task(request_data, user_id, task_type):
    # 请求数据
    data = request_data.dict()

    args = {"data": data, "user_id": user_id, "task_type": task_type}

    # timestamp = time.time()
    # if request_data.vip:
    #     # 将任务发送到 Celery 队列
    #     result = high_priority_task.delay(args)
    #     # 将 task_id 和当前时间戳添加到 Redis 有序集合
    #     task_id = result.id
    #     redis_client.zadd("high_task_queue", {task_id: timestamp})
    # else:
    #     # 将任务发送到 Celery 队列
    #     result = low_priority_task.delay(args)
    #     # 将 task_id 和当前时间戳添加到 Redis 有序集合
    #     task_id = result.id
    #     redis_client.zadd("low_task_queue", {task_id: timestamp})
    #
    # return result.id
    if request_data.vip:
        priority = 1
    else:
        priority = 10

    result = generate_task.apply_async((args, 1), queue="facefusion_queue", priority=priority)
    return result.id


@router.post("/generate")
async def generate(request: GenerateRequest, user_id: int = Depends(get_current_user_id),
                   db: Session = Depends(get_db)):
    task_id = create_generate_task(request, user_id, task_type='image')
    add_task(user_id, task_id, db)
    return {"task_id": task_id}


@router.post("/generate_video")
async def generate_video(request: VideoGenerateRequest, user_id: int = Depends(get_current_user_id),
                         db: Session = Depends(get_db)):
    task_id = create_generate_task(request, user_id, task_type='video')
    add_task(user_id, task_id, db)
    return {"task_id": task_id}


@router.post("/upscale")
async def upscale(request: UpscaleRequest, user_id: int = Depends(get_current_user_id),
                  db: Session = Depends(get_db)):
    task_id = create_generate_task(request, user_id, task_type='upscale')
    add_task(user_id, task_id, db)
    return {"task_id": task_id}


@router.get("/generate/{task_id}")
async def generate_status(task_id: str, user_id: int = Depends(get_current_user_id)):
    # result = AsyncResult(task_id, app=high_priority_task.app)
    #
    # if result.ready():
    #     return {"status": "SUCCESS"}
    # else:
    #     # 获取任务在有序集合中的排名（从 0 开始）
    #     rank = redis_client.zrank("high_task_queue", task_id)
    #     if rank is None:
    #         high_task_queue_length = redis_client.zcard("high_task_queue")
    #
    #         rank = redis_client.zrank("low_task_queue", task_id)
    #         if rank is None:
    #             raise HTTPException(status_code=404, detail="Task not found in queue")
    #         else:
    #             if result.state == "STARTED":
    #                 position = 0
    #             else:
    #                 position = high_task_queue_length + rank
    #
    #             vip_type = "normal"
    #     else:
    #         position = rank
    #         vip_type = "vip"
    #
    #     return {"status": result.state, "type": vip_type, "position": position}  # 排名从 1 开始

    result = AsyncResult(task_id, app=generate_task.app)
    if result.ready():
        return {"status": "SUCCESS"}
    else:
        task_list = redis_client.lrange("facefusion_queue", 0, -1)
        for task in task_list:
            print(task.decode())

        return {"status": result.state, "position": 1}
        # # 获取队列中的所有任务
        # task_list = redis_client.lrange("facefusion_queue", 0, -1)
        # # 查找任务位置
        # for index, task in enumerate(task_list):
        #     if task_id in task.decode('utf-8'):
        #         position = index + 1
        #         print(f"Task {task_id} is at position {position} in the queue.")
        #         return {"status": result.state, "position": position}

        # raise HTTPException(status_code=404, detail="Task not found in queue")
