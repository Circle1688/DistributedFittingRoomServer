import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import UploadFile, File

from plugin_server.auth import get_current_user_id
from plugin_server.utils import *

router = APIRouter()


def suggest_avatar_name(user_id, thumbnail=False):
    if thumbnail:
        return f'{user_id}/avatar/avatar_thumbnail.jpg'
    return f'{user_id}/avatar/avatar.png'


def get_avatar_filepath(user_id):
    return get_full_url_oss(suggest_avatar_name(user_id))


def suggest_file_name(user_id, file_name):
    return f'{user_id}/gallery/{file_name}'


def upload_avatar_task(user_id, file_obj):
    avatar_path = suggest_avatar_name(user_id)
    # 生成缩略图
    thumbnail_obj = compress_image_bytes(file_obj, 100, 200)
    thumbnail_file_path = suggest_avatar_name(user_id, thumbnail=True)

    if upload_obj_oss(file_obj, avatar_path) and upload_obj_oss(thumbnail_obj, thumbnail_file_path):
        return {"avatar_url": get_full_url_oss(avatar_path),
                "avatar_thumbnail_url": get_full_url_oss(thumbnail_file_path)}
    else:
        return None


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
    avatar_path = f'{user_id}/avatar/avatar.png'
    loop = asyncio.get_event_loop()
    last_modified = await loop.run_in_executor(None, get_last_modified, avatar_path)
    return {"avatar_url": get_avatar_filepath(user_id),
            "avatar_thumbnail_url": get_full_url_oss(suggest_avatar_name(user_id, thumbnail=True)),
            "last_modified": last_modified}


@router.get('/get_gallery')
async def get_gallery(user_id: int = Depends(get_current_user_id)):
    files = get_files_oss(f'{user_id}/gallery/')

    gallery_urls = []
    for file, last_modified in files:
        if not file.endswith("_thumbnail.jpg"):
            gallery_urls.append({"source_url": file,
                                 "thumbnail_url": file.rsplit('.', 1)[0] + "_thumbnail.jpg",
                                 "last_modified": last_modified})

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
