import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import UploadFile, File
from sqlalchemy import desc

from plugin_server.auth import get_current_user_id
from plugin_server.models import Gallery
from plugin_server.schemas import GalleryRequest
from plugin_server.utils import *
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/upload_avatar')
async def upload_avatar(file: UploadFile = File(...), user_id: int = Depends(get_current_user_id)):
    file_obj = await file.read()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, upload_avatar_task, user_id, file_obj)
    if result:
        return result
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/get_avatar')
async def get_avatar(user_id: int = Depends(get_current_user_id)):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, get_avatar_task, user_id)
    if result:
        return {"avatar_url": get_full_url_oss(result["avatar_path"]),
                "avatar_thumbnail_url": get_full_url_oss(result["thumbnail_avatar_path"])}
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/get_gallery')
async def get_gallery(limit: int, cursor: Optional[int] = None, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_gallery = db.query(Gallery).filter_by(user_id=user_id)
    if cursor:
        db_gallery = db_gallery.filter(Gallery.last_modified < cursor)

    photos = db_gallery.order_by(desc(Gallery.last_modified)).limit(limit).all()

    next_cursor = photos[-1].last_modified if photos else None
    has_next = len(photos) == limit

    ret_data = {
        "gallery_urls": [{"source_url": p.source_url, "thumbnail_url": p.thumbnail_url, "last_modified": p.last_modified} for p in photos],
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor,
            "has_next": has_next
        }
    }

    return ret_data


@router.delete('/remove_gallery_file/{file_name}')
async def remove_gallery_file(file_name: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        source_file = f'{user_id}/gallery/{file_name}'
        thumbnail_filename = f"{os.path.basename(source_file)}_thumbnail.jpg"

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, batch_delete_obj_oss, [source_file, thumbnail_filename])
        if result:
            db_gallery = db.query(Gallery).filter_by(user_id=user_id, source_url=get_full_url_oss(source_file)).first()
            if db_gallery:
                db.delete(db_gallery)
                db.commit()
                return {"message": f"{file_name} removed successfully"}
        else:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f'Remove gallery file failed: {e}')
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/upload_files')
async def upload_files(request: GalleryRequest, db: Session = Depends(get_db)):
    try:
        user_id = request.user_id
        source_url = request.source_url
        thumbnail_url = request.thumbnail_url
        last_modified = int(time.time())
        new_gallery = Gallery(user_id=user_id, source_url=source_url, thumbnail_url=thumbnail_url, last_modified=last_modified)
        db.add(new_gallery)
        db.commit()
        db.refresh(new_gallery)
        return {"message": "ok"}
    except Exception as e:
        print(f'Upload files to database failed: {e}')
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
