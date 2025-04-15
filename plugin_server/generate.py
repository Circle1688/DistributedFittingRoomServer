from plugin_server.facefusion import facefusion_image, facefusion_image_internal, facefusion_video
from plugin_server.pixverse import pixverse_process
from plugin_server.ue import ue_process
from plugin_server.upscale import upscale_process

from plugin_server.utils import *

from plugin_server.try_on import virtual_try_on


# 创建临时文件夹
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

TEMP_OUTPUT_DIR = os.path.join(TEMP_DIR, 'output')
if not os.path.exists(TEMP_OUTPUT_DIR):
    os.mkdir(TEMP_OUTPUT_DIR)

TEMP_DOWNLOAD_DIR = os.path.join(TEMP_DIR, 'download')
if not os.path.exists(TEMP_DOWNLOAD_DIR):
    os.mkdir(TEMP_DOWNLOAD_DIR)


def upload_files(folder, user_id):
    files = []
    for file in get_files(folder):
        file_name = suggest_file_name(user_id, file['filename'])

        if not upload_file_oss(file['filepath'], file_name):
            # 如果上传失败
            return False
        if not file_name.endswith("_thumbnail.jpg"):
            file_url = get_full_url_oss(file_name)

            url = f'http://{SERVER_HOST}:8000/upload_files'

            data = {
                'user_id': user_id,
                'source_url': file_url,
                'thumbnail_url': file_url.rsplit('.', 1)[0] + "_thumbnail.jpg"
            }

            response = requests.post(url, json=data)

            if response.status_code != 200:
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
        print("[Update Task Status] Success")
        return True

    print("[Update Task Status] Failed")
    return False


def process_upscale(video_url, output_path, task_id, user_id):
    # 下载视频
    input_path = download_file(video_url, download_dir=TEMP_DOWNLOAD_DIR)

    video_output_path = os.path.join(output_path, f'{task_id}_upscale.mp4')

    if upscale_process(input_path, video_output_path):
        # 生成视频缩略图
        extract_video_cover(video_output_path)
        # 上传到oss
        return upload_files(output_path, user_id)
    return False


def process_facefusion_image(request_data, source_image_path, ue_images_folder, output_path, task_id, user_id):
    # facefusion图像
    if facefusion_image(task_id, source_image_path, ue_images_folder, output_path, request_data['image_options']):

        render_mode = request_data['render_mode']
        if render_mode != "3D":
            # 虚拟试穿
            for file in get_files(output_path):
                if not file['filename'].endswith("_thumbnail.jpg"):
                    human_image_path = file['filepath']
                    if not virtual_try_on(render_mode, human_image_path, request_data):
                        return False

                    # 压缩
                    img = Image.open(human_image_path)

                    # 以指定质量保存压缩后的结果
                    img.save(human_image_path, quality=100)

                    # 生成缩略图
                    image_options = request_data['image_options']
                    quality = image_options['quality']
                    thumbnail_width = image_options['thumbnail_width']

                    compress_image(human_image_path, quality, thumbnail_width)

        # 上传到oss
        return upload_files(output_path, user_id)


def process_pre_video(request_data, source_image_path, ue_images_folder):
    target_image_path = find_png_files(ue_images_folder)[0]

    image_output_path = os.path.join(TEMP_DIR, 'temp.png')

    # 首次换脸
    first_result, image_output_path = facefusion_image_internal(source_image_path, target_image_path,
                                                                image_output_path)
    # 首次换脸成功
    if first_result:

        # 渲染模式
        render_mode = request_data['render_mode']

        if render_mode != "3D":
            # 虚拟试穿
            if not virtual_try_on(render_mode, image_output_path, request_data):
                return None

        return image_output_path
    else:
        return None


def generate_process(task_id, args):
    user_id = args["user_id"]
    result = False
    try:
        # 更新任务状态
        update_task_status(user_id, task_id, "STARTED")

        start_time = time.time()
        server_logger.info(f"[{task_id}] Start process...")

        # 输出路径
        output_path = TEMP_OUTPUT_DIR

        # 清除输出目录
        clear_folder(output_path)

        task_type = args['task_type']

        # upscale
        if task_type == "upscale":
            video_url = args["data"]["video_url"]
            result = process_upscale(video_url, output_path, task_id, user_id)

        else:
            # 下载头像
            source_image_path = download_avatar(user_id)

            # 头像获取成功
            if source_image_path:
                request_data = args["data"]

                server_logger.info("UE...")
                # UE生成图像
                ue_images_folder = ue_process(request_data)

                if task_type == "image":
                    server_logger.info("FaceFusion image...")
                    # facefusion图像
                    result = process_facefusion_image(request_data, source_image_path, ue_images_folder, output_path, task_id, user_id)

                else:
                    # pixverse的流程
                    pre_video = False
                    pixverse_input_image_path = None

                    if task_type == "video":
                        server_logger.info("Pre swap face...")
                        pixverse_input_image_path = process_pre_video(request_data, source_image_path, ue_images_folder)
                        if pixverse_input_image_path:
                            pre_video = True

                    elif task_type == "image_to_video":
                        # 下载图片
                        image_url = args["data"]["image"]
                        pixverse_input_image_path = download_file(image_url, download_dir=TEMP_DOWNLOAD_DIR)
                        pre_video = True

                    if pre_video:
                        server_logger.info("PixVerse...")
                        # 处理视频
                        video_path = os.path.join(TEMP_DIR, 'temp.mp4')
                        if pixverse_process(pixverse_input_image_path, video_path, request_data['video_options']):
                            server_logger.info("Process video...")

                            # 视频换脸
                            video_output_path = facefusion_video(task_id, source_image_path, video_path, output_path)
                            if video_output_path:
                                # 生成视频缩略图
                                extract_video_cover(video_output_path)
                                # 上传到oss
                                result = upload_files(output_path, user_id)

        end_time = round(time.time() - start_time, 2)
        server_logger.info(f"[{task_id}] Finish process in {end_time} seconds.")

        update_task_status(user_id, task_id, "SUCCESS" if result else "FAILED")

        return result
    except Exception as e:
        server_logger.info(f"[Generate] Error: {e}")
        update_task_status(user_id, task_id, "SUCCESS" if result else "FAILED")
        return False
