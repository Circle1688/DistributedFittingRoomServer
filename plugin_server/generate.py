import time
import requests

from plugin_server.config import SERVER_HOST
from plugin_server.logger import server_logger

from plugin_server.facefusion import facefusion_image, facefusion_image_internal, facefusion_video
from plugin_server.pixverse import pixverse_process
from plugin_server.ue import ue_process
from plugin_server.upscale import upscale_process

from plugin_server.utils import *


# 创建临时文件夹
TEMP_DIR = './.temp'
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

TEMP_OUTPUT_DIR = os.path.join(TEMP_DIR, 'output')
if not os.path.exists(TEMP_OUTPUT_DIR):
    os.mkdir(TEMP_OUTPUT_DIR)


def download_avatar(user_id):
    url = f'http://{SERVER_HOST}:8000/get_avatar_internal/{user_id}'
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        filename = os.path.join(TEMP_DIR, "avatar.jpg")
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filename
    else:
        return None


def download_video(user_id, url):
    get_url = f'http://{SERVER_HOST}:8000/get_gallery_video_internal/{user_id}/{url}'
    response = requests.get(get_url, stream=True)

    if response.status_code == 200:
        filename = os.path.join(TEMP_DIR, "source.mp4")
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filename
    else:
        return None


def upload_files(user_id, upload_folder):
    url = f'http://{SERVER_HOST}:8000/upload_files'

    files = []

    for file in get_files(upload_folder):
        files.append(('files', (file['filename'], open(file['filepath'], 'rb'))))

    data = {'user_id': user_id}

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        server_logger.info("[Upload Result] Success")
        return True

    server_logger.info("[Upload Result] Failed")
    return False


def update_task_status(user_id, task_id, status):
    url = f'http://{SERVER_HOST}:8000/update_task_status'

    data = {
        'user_id': user_id,
        'task_id': task_id,
        'status': status
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        server_logger.info("[Update Task Status] Success")
        return True

    server_logger.info("[Update Task Status] Failed")
    return False


def generate_process(task_id, args):
    user_id = args["user_id"]

    # 更新任务状态
    update_task_status(user_id, task_id, "STARTED")

    start_time = time.time()
    server_logger.info(f"[{task_id}] Start process...")

    # 输出路径
    output_path = TEMP_OUTPUT_DIR

    # 清除输出目录
    clear_folder(output_path)

    task_type = args['task_type']
    if task_type == "upscale":
        video_url = args["data"]["video_url"]
        input_path = download_video(user_id, video_url)
        video_output_path = os.path.join(output_path, task_id + "_upscale.mp4")

        if upscale_process(input_path, video_output_path):
            result = upload_files(user_id, output_path)
        else:
            result = False

    else:
        # 头像
        source_image_path = download_avatar(user_id)

        # 头像获取失败
        if source_image_path is None:
            result = False
        else:
            request_data = args["data"]

            server_logger.info("UE...")
            # UE生成图像
            images_folder = ue_process(request_data)

            if task_type == "image":
                server_logger.info("FaceFusion image...")
                # facefusion图像
                if facefusion_image(task_id, source_image_path, images_folder, output_path, request_data['image_options']):
                    result = upload_files(user_id, output_path)
                else:
                    result = False

            elif task_type == "video":
                target_image_path = find_png_files(images_folder)[0]

                image_output_path = os.path.join(TEMP_DIR, 'temp.png')

                server_logger.info("Pre swap face...")
                # 首次换脸
                first_result, image_output_path = facefusion_image_internal(source_image_path, target_image_path,
                                                                            image_output_path)
                # 首次换脸成功
                if first_result:
                    server_logger.info("PixVerse...")
                    # 处理视频
                    video_path = os.path.join(TEMP_DIR, 'temp.mp4')
                    if pixverse_process(image_output_path, video_path, request_data['video_options']):
                        server_logger.info("Process video...")

                        # 视频换脸
                        if facefusion_video(task_id, source_image_path, video_path, output_path):
                            result = upload_files(user_id, output_path)
                        else:
                            result = False
                    else:
                        result = False
                else:
                    result = False
            else:
                result = False

    end_time = round(time.time() - start_time, 2)
    server_logger.info(f"[{task_id}] Finish process in {end_time} seconds.")

    update_task_status(user_id, task_id, "SUCCESS" if result else "FAILED")

    return result
