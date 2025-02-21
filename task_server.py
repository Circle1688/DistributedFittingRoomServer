import json
import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status

from plugin_server.config import *
from plugin_server.database_func import Session, get_db
from plugin_server.models import TaskStorage

app = FastAPI()

@app.get("/get_all_queue_tasks")
async def get_all_queue_tasks(db: Session = Depends(get_db)):
    pending_tasks_count = db.query(TaskStorage).filter_by(status="PENDING").count()
    started_tasks_count = db.query(TaskStorage).filter_by(status="STARTED").count()

    return {"pending_tasks_count": pending_tasks_count, "started_tasks_count": started_tasks_count}


@app.get("/get_system_status")
async def get_system_status():
    try:
        status_file_path = os.path.join(SYSTEM_MANAGER_PATH, 'status.json')
        if os.path.exists(status_file_path):
            with open(status_file_path, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
                return status_data
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status file not found")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8010)
