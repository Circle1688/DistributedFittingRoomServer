import time
from fastapi import APIRouter, Depends, HTTPException, status
from plugin_server.schemas import *
from plugin_server.auth import get_current_user_id
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session

from faceswap.tasks import high_priority_task, low_priority_task, redis_client
from celery.result import AsyncResult
from faceswap.celery import app

from plugin_server.task_routes import add_task, check_limit

router = APIRouter()


def create_generate_task(request_data, user_id, task_type):
    # 请求数据
    data = request_data.dict()

    args = {"data": data, "user_id": user_id, "task_type": task_type}

    timestamp = time.time()
    if data["task_options"]["vip"]:
        # 将任务发送到 Celery 队列
        result = high_priority_task.apply_async((args,), queue="facefusion_queue", priority=1)
        # 将 task_id 和当前时间戳添加到 Redis 有序集合
        task_id = result.id
        redis_client.zadd("high_task_queue", {task_id: timestamp})
    else:
        # 将任务发送到 Celery 队列
        result = low_priority_task.apply_async((args,), queue="facefusion_queue", priority=10)
        # 将 task_id 和当前时间戳添加到 Redis 有序集合
        task_id = result.id
        redis_client.zadd("low_task_queue", {task_id: timestamp})

    return result.id


@router.post("/generate")
async def generate(request: GenerateRequest, user_id: int = Depends(get_current_user_id),
                   db: Session = Depends(get_db)):
    if check_limit(user_id, request, db):
        task_id = create_generate_task(request, user_id, task_type='image')
        add_task(user_id, task_id, db)
        return {"task_id": task_id}
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="The number of user tasks exceeded the limit")


@router.post("/generate_video")
async def generate_video(request: VideoGenerateRequest, user_id: int = Depends(get_current_user_id),
                         db: Session = Depends(get_db)):
    if check_limit(user_id, request, db):
        task_id = create_generate_task(request, user_id, task_type='video')
        add_task(user_id, task_id, db)
        return {"task_id": task_id}
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="The number of user tasks exceeded the limit")


@router.post("/upscale")
async def upscale(request: UpscaleRequest, user_id: int = Depends(get_current_user_id),
                  db: Session = Depends(get_db)):
    if check_limit(user_id, request, db):
        task_id = create_generate_task(request, user_id, task_type='upscale')
        add_task(user_id, task_id, db)
        return {"task_id": task_id}
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="The number of user tasks exceeded the limit")


@router.post("/image_to_video")
async def image_to_video(request: ImageToVideoRequest, user_id: int = Depends(get_current_user_id),
                         db: Session = Depends(get_db)):
    if check_limit(user_id, request, db):
        task_id = create_generate_task(request, user_id, task_type='image_to_video')
        add_task(user_id, task_id, db)
        return {"task_id": task_id}
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="The number of user tasks exceeded the limit")



@router.get("/generate/{task_id}")
async def generate_status(task_id: str, user_id: int = Depends(get_current_user_id)):
    result = AsyncResult(task_id, app=app)
    if result.ready():
        task_result = result.get()
        return {"status": "SUCCESS" if task_result else "FAILED"}

    elif result.state == "STARTED":
        return {"status": result.state, "position": 0}
    else:
        # 获取任务在有序集合中的排名（从 0 开始）
        rank = redis_client.zrank("high_task_queue", task_id)
        if rank is None:
            # vip队列数量
            high_task_queue_length = redis_client.zcard("high_task_queue")
            # 普通队列排名，从0开始排名
            rank = redis_client.zrank("low_task_queue", task_id)
            if rank is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found in queue")
            else:
                # 加上vip数量
                # 因为是从0开始，所以要+1
                position = rank + 1
                position += high_task_queue_length
                return {"status": result.state, "type": "normal", "position": position}
        else:
            # 因为是从0开始，所以要+1
            position = rank + 1
            return {"status": result.state, "type": "vip", "position": position}  # 排名从 1 开始
