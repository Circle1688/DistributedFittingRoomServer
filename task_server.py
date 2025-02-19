import uvicorn
from fastapi import FastAPI, Depends

from plugin_server.database_func import Session, get_db
from plugin_server.models import TaskStorage

app = FastAPI()

@app.get("/get_all_queue_tasks")
async def get_all_queue_tasks(db: Session = Depends(get_db)):
    pending_tasks_count = db.query(TaskStorage).filter_by(status="PENDING").count()
    started_tasks_count = db.query(TaskStorage).filter_by(status="STARTED").count()

    return {"pending_tasks_count": pending_tasks_count, "started_tasks_count": started_tasks_count}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8010)
