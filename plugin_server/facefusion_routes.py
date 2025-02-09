import os
import time

from fastapi import APIRouter, Depends, HTTPException, status

from plugin_server.gallery_routes import get_avatar_filepath
from plugin_server.schemas import *
from plugin_server.auth import get_current_user_id
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session

from faceswap.tasks import high_priority_task, low_priority_task, redis_client
from celery.result import AsyncResult

from plugin_server.task_routes import add_task

router = APIRouter()


def create_generate_task(request_data, user_id, is_video):
    # 请求数据
    ue_json_data = request_data.dict()

    args = {"ue_json_data": ue_json_data, "user_id": user_id, "video": is_video}

    timestamp = time.time()
    if request_data.vip:
        # 将任务发送到 Celery 队列
        result = high_priority_task.delay(args)
        # 将 task_id 和当前时间戳添加到 Redis 有序集合
        task_id = result.id
        redis_client.zadd("high_task_queue", {task_id: timestamp})
    else:
        # 将任务发送到 Celery 队列
        result = low_priority_task.delay(args)
        # 将 task_id 和当前时间戳添加到 Redis 有序集合
        task_id = result.id
        redis_client.zadd("low_task_queue", {task_id: timestamp})

    return result.id


@router.post("/generate")
async def generate(request: GenerateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # 获取头像
    source_image_path = get_avatar_filepath(user_id)

    if not os.path.exists(source_image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

    task_id = create_generate_task(request, user_id, is_video=False)
    add_task(user_id, task_id, db)
    return {"task_id": task_id}


@router.post("/generate_video")
async def generate_video(request: VideoGenerateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # 获取头像
    source_image_path = get_avatar_filepath(user_id)

    if not os.path.exists(source_image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

    task_id = create_generate_task(request, user_id, is_video=True)
    add_task(user_id, task_id, db)
    return {"task_id": task_id}


@router.get("/generate/{task_id}")
async def generate_status(task_id: str, user_id: int = Depends(get_current_user_id)):
    result = AsyncResult(task_id, app=high_priority_task.app)

    if result.ready():
        return {"status": "SUCCESS"}
    else:
        # 获取任务在有序集合中的排名（从 0 开始）
        rank = redis_client.zrank("high_task_queue", task_id)
        if rank is None:
            high_task_queue_length = redis_client.zcard("high_task_queue")

            rank = redis_client.zrank("low_task_queue", task_id)
            if rank is None:
                raise HTTPException(status_code=404, detail="Task not found in queue")
            else:
                position = high_task_queue_length + rank
                task_type = "normal"
        else:
            position = rank
            task_type = "vip"

        return {"status": result.state, "type": task_type, "position": position}  # 排名从 1 开始
