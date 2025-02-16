import time
from plugin_server.config import SERVER_HOST
from plugin_server.gallery_routes import suggest_file_name, get_avatar_filepath
from plugin_server.logger import server_logger

from plugin_server.facefusion import facefusion_image, facefusion_image_internal, facefusion_video
from plugin_server.oss import upload_file_oss
from plugin_server.pixverse import pixverse_process
from plugin_server.ue import ue_process
from plugin_server.upscale import upscale_process

from plugin_server.utils import *


# 创建临时文件夹
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

TEMP_OUTPUT_DIR = os.path.join(TEMP_DIR, 'output')
if not os.path.exists(TEMP_OUTPUT_DIR):
    os.mkdir(TEMP_OUTPUT_DIR)


def upload_files_oss(folder, user_id):
    for file in get_files(folder):
        if not upload_file_oss(file['filepath'], suggest_file_name(user_id, file['filename'])):
            return False
    return True


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
    result = False
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
        # 下载视频
        input_path = download_file(video_url)

        video_output_path = os.path.join(output_path, f'{task_id}_upscale.mp4')

        if upscale_process(input_path, video_output_path):
            # 生成视频缩略图
            extract_video_cover(video_output_path)
            # 上传到oss
            result = upload_files_oss(output_path, user_id)

    else:
        # 获取头像url
        avatar_url = get_avatar_filepath(user_id)
        # 下载头像
        source_image_path = download_file(avatar_url)

        # 头像获取成功
        if source_image_path:
            request_data = args["data"]

            server_logger.info("UE...")
            # UE生成图像
            images_folder = ue_process(request_data)

            if task_type == "image":
                server_logger.info("FaceFusion image...")
                # facefusion图像
                if facefusion_image(task_id, source_image_path, images_folder, output_path, request_data['image_options']):
                    # 上传到oss
                    result = upload_files_oss(output_path, user_id)

            elif task_type == "video":
                target_image_path = find_png_files(images_folder)[0]

                image_output_path = os.path.join(TEMP_DIR, 'temp.png')

                server_logger.info("Pre swap face...")
                # 首次换脸
                first_result, image_output_path = facefusion_image_internal(source_image_path, target_image_path, image_output_path)
                # 首次换脸成功
                if first_result:
                    server_logger.info("PixVerse...")
                    # 处理视频
                    video_path = os.path.join(TEMP_DIR, 'temp.mp4')
                    if pixverse_process(image_output_path, video_path, request_data['video_options']):
                        server_logger.info("Process video...")

                        # 视频换脸
                        video_output_path = facefusion_video(task_id, source_image_path, video_path, output_path)
                        if video_output_path:
                            # 生成视频缩略图
                            extract_video_cover(video_output_path)
                            # 上传到oss
                            result = upload_files_oss(output_path, user_id)

    end_time = round(time.time() - start_time, 2)
    server_logger.info(f"[{task_id}] Finish process in {end_time} seconds.")

    update_task_status(user_id, task_id, "SUCCESS" if result else "FAILED")

    return result
