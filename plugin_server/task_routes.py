from fastapi import APIRouter, Depends, HTTPException, status
from plugin_server.models import *
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session
from plugin_server.auth import get_current_user_id
from plugin_server.schemas import TaskRequest

router = APIRouter()


def add_task(user_id, task_id, db: Session):
    # 添加用户任务
    new_task = TaskStorage(user_id=user_id, task_id=task_id, status="PENDING")
    db.add(new_task)
    db.commit()
    db.refresh(new_task)


@router.post("/update_task_status")
def update_task_status(task: TaskRequest, db: Session = Depends(get_db)):
    db_task = db.query(TaskStorage).filter_by(user_id=task.user_id, task_id=task.task_id).first()
    if db_task:
        db_task.status = task.status
        db.commit()
        return {"message": f"Task {task.task_id} status updated to {task.status} for user {task.user_id}."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found")


@router.get("/get_tasks")
async def get_tasks(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):

    tasks = db.query(TaskStorage).filter_by(user_id=user_id).all()
    if tasks:
        tasks_list = []
        for task in tasks:
            tasks_list.append({"taskid": task.task_id, "status": task.status})

        return {"tasks": tasks_list}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found")
