import os

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import UploadFile, File, Response
from fastapi.responses import FileResponse

from plugin_server.config import *
from plugin_server.auth import get_current_user_id
from plugin_server.utils import get_sorted_files, compress_image

router = APIRouter()


def get_avatar_dir(user_id):
    # 获取头像目录路径
    return os.path.join(USER_DATA_DIR, f"{str(user_id)}/avatar/")


def get_avatar_filepath(user_id, thumbnail=False):
    # 获取头像路径
    store_dir = os.path.join(USER_DATA_DIR, f"{str(user_id)}/avatar/")
    if not os.path.exists(store_dir):
        os.makedirs(store_dir)

    if thumbnail:
        filename = f"{user_id}_avatar_thumbnail.jpg"
    else:
        filename = f"{user_id}_avatar.png"
    filepath = os.path.join(store_dir, filename)
    return filepath


def get_gallery_dir(user_id):
    # 获取图库路径
    return os.path.join(USER_DATA_DIR, f"{str(user_id)}/gallery/")


@router.post('/upload_avatar')
async def upload_avatar(file: UploadFile = File(...), user_id: int = Depends(get_current_user_id)):
    # 确保上传目录存在
    store_dir = get_avatar_dir(user_id)
    if not os.path.exists(store_dir):
        os.makedirs(store_dir)

    filepath = get_avatar_filepath(user_id)

    # 保存文件到服务器
    async with aiofiles.open(filepath, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
        # 生成缩略图
        compress_image(filepath, 100, 200)

    return {"message": "Uploaded avatar successfully"}


@router.get('/get_avatar')
async def get_avatar(user_id: int = Depends(get_current_user_id)):
    # 获取文件路径
    filepath = get_avatar_filepath(user_id)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

    async with aiofiles.open(filepath, "rb") as image_file:
        image_data = await image_file.read()

    return Response(content=image_data, media_type="image/jpeg")


@router.get('/get_avatar_thumbnail')
async def get_avatar_thumbnail(user_id: int = Depends(get_current_user_id)):
    # 获取文件路径
    filepath = get_avatar_filepath(user_id, thumbnail=True)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar thumbnail not found")

    async with aiofiles.open(filepath, "rb") as image_file:
        image_data = await image_file.read()

    return Response(content=image_data, media_type="image/jpeg")


@router.get('/get_gallery')
async def get_gallery(user_id: int = Depends(get_current_user_id)):
    store_dir = get_gallery_dir(user_id)

    if not os.path.exists(store_dir):
        return {"gallery_urls": []}

    files = get_sorted_files(store_dir)

    gallery_urls = []
    for file in files:
        if not file.lower().endswith("_thumbnail.jpg"):
            if file.lower().endswith(".jpg"):
                file_type = "image"
            elif file.lower().endswith(".mp4"):
                file_type = "video"
            else:
                continue

            gallery_urls.append({"type": file_type, "url": file.split('.')[0]})

    return {"gallery_urls": gallery_urls}


@router.get('/get_gallery_image/{url}')
async def get_gallery_image(url: str, user_id: int = Depends(get_current_user_id)):
    url += ".jpg"
    # 读取文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    async with aiofiles.open(filepath, "rb") as image_file:
        image_data = await image_file.read()

    return Response(content=image_data, media_type="image/jpeg")


@router.get('/get_gallery_video/{url}')
async def get_gallery_video(url: str, user_id: int = Depends(get_current_user_id)):
    url += ".mp4"
    # 读取文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    return FileResponse(filepath, media_type="video/mp4", filename=f"{url}.mp4")


@router.get('/get_thumbnail/{url}')
async def get_thumbnail(url: str, user_id: int = Depends(get_current_user_id)):
    url += "_thumbnail.jpg"
    # 读取文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    async with aiofiles.open(filepath, "rb") as image_file:
        image_data = await image_file.read()

    return Response(content=image_data, media_type="image/jpeg")


@router.delete('/remove_gallery_image/{url}')
async def remove_gallery_image(url: str, user_id: int = Depends(get_current_user_id)):
    # 删除服务器上的文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)
    if os.path.exists(filepath + ".jpg"):
        os.remove(filepath + ".jpg")
        if os.path.exists(filepath + "_thumbnail.jpg"):
            os.remove(filepath + "_thumbnail.jpg")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found in gallery")

    return {"message": f"{url} removed successfully"}


@router.delete('/remove_gallery_video/{url}')
async def remove_gallery_video(url: str, user_id: int = Depends(get_current_user_id)):
    # 删除服务器上的文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)
    if os.path.exists(filepath + ".mp4"):
        os.remove(filepath + ".mp4")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found in gallery")

    return {"message": f"{url} removed successfully"}


@router.get('/get_avatar_internal/{user_id}')
async def get_avatar_internal(user_id: str):
    # 内部节点，用来给worker获取头像的
    # 获取文件路径
    filepath = get_avatar_filepath(user_id)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

    async with aiofiles.open(filepath, "rb") as image_file:
        image_data = await image_file.read()

    return Response(content=image_data, media_type="image/jpeg")


@router.get('/get_gallery_video_internal/{user_id}/{url}')
async def get_gallery_video_internal(user_id: str, url: str):
    url += ".mp4"
    # 读取文件
    store_dir = get_gallery_dir(user_id)
    filepath = os.path.join(store_dir, url)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    return FileResponse(filepath, media_type="video/mp4", filename=f"{url}.mp4")


@router.post('/upload_files')
async def upload_files(user_id: str = Form(...), files: list[UploadFile] = File(...)):
    # 内部节点，用来给worker回传结果的
    save_path = get_gallery_dir(user_id)

    for file in files:
        file_path = os.path.join(save_path, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

    return {"filenames": [file.filename for file in files], "save_path": save_path}
