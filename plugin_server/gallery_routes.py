import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import UploadFile, File

from plugin_server.auth import get_current_user_id
from plugin_server.utils import *

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
async def get_gallery(user_id: int = Depends(get_current_user_id)):
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, get_files_oss, f'{user_id}/gallery/')

    start_time = time.time()

    gallery_urls = []
    for file, last_modified in files:
        if not file.endswith("_thumbnail.jpg"):
            gallery_urls.append({"source_url": file,
                                 "thumbnail_url": file.rsplit('.', 1)[0] + "_thumbnail.jpg",
                                 "last_modified": last_modified})

    print(round(time.time() - start_time, 2))

    return {"gallery_urls": gallery_urls}


@router.delete('/remove_gallery_file/{file_name}')
async def remove_gallery_file(file_name: str, user_id: int = Depends(get_current_user_id)):
    source_file = f'{user_id}/gallery/{file_name}'
    thumbnail_filename = f"{os.path.basename(source_file)}_thumbnail.jpg"

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, batch_delete_obj_oss, [source_file, thumbnail_filename])
    if result:
        return {"message": f"{file_name} removed successfully"}
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
