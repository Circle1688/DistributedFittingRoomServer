import json
import time
import uuid

import requests

from plugin_server.config import PIXVERSE_API_KEY
from plugin_server.logger import server_logger

PIXVERSE_POLLING_INTERVAL = 3

def pixverse_upload_image(image_path):
    url = "https://app-api.pixverse.ai/openapi/v2/image/upload"

    with open(image_path, "rb") as f:
        files = {
            "image": (image_path, f, "application/octet-stream")
        }
        headers = {
            'API-KEY': PIXVERSE_API_KEY,
            'Ai-trace-id': str(uuid.uuid4())
        }
        response = requests.request("POST", url, headers=headers, files=files)

    if response.status_code == 200:
        rsp = response.json()
        img_id = rsp['Resp']['img_id']
        server_logger.info("[PixVerse] Uploaded image successfully")
        return True, img_id

    elif response.status_code == 500:
        rsp = response.json()
        print(rsp)
        server_logger.info("[PixVerse] Uploaded image content moderation failed.")
        return False, None


def pixverse_image_to_video(img_id, args):
    url = "https://app-api.pixverse.ai/openapi/v2/video/img/generate"

    payload = json.dumps({
        "duration": args['duration'],
        "img_id": img_id,
        "model": "v3.5",
        "motion_mode": "normal",
        "negative_prompt": args['negative_prompt'],
        "prompt": args['prompt'],
        "quality": "360p",
        "seed": args['seed'],
        "water_mark": False
    })
    headers = {
        'API-KEY': PIXVERSE_API_KEY,
        'Ai-trace-id': str(uuid.uuid4()),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    rsp = response.json()

    return rsp['Resp']['video_id']


def pixverse_get_result(video_id):
    while True:
        url = f"https://app-api.pixverse.ai/openapi/v2/video/result/{video_id}"

        payload = {}
        headers = {
            'API-KEY': PIXVERSE_API_KEY,
            'Ai-trace-id': str(uuid.uuid4())
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        rsp = response.json()

        status = rsp['Resp']['status']

        # 1: Generation successful; 5: Generating; 7: Contents moderation failed; 8: Generation failed;
        if status == 1:
            server_logger.info("[PixVerse] Generation successful.")
            video_url = rsp['Resp']['url']
            return True, video_url
        elif status == 7:
            server_logger.info("[PixVerse] Contents moderation failed.")
            return False, None
        elif status == 8:
            server_logger.info("[PixVerse] Generation failed.")
            return False, None
        elif status == 5:
            server_logger.info("[PixVerse] Generating")
            time.sleep(PIXVERSE_POLLING_INTERVAL)
        else:
            return False, None



def download_video(url, save_path):
    try:
        # 发起 GET 请求
        response = requests.get(url, stream=True)

        # 打开本地文件，以二进制写入模式
        with open(save_path, 'wb') as file:
            # 分块写入文件，避免占用过多内存
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        server_logger.info("[PixVerse] Download Video successfully")
        return True
    except Exception as e:
        server_logger.info(f"[PixVerse] [Download Video] {e}")
        return False


def pixverse_process(image_path, video_path, args):
    start_time = time.time()
    if args["pixverse"]:
        # 上传图片
        result, img_id = pixverse_upload_image(image_path)

        # 上传成功
        if result:
            # 生成视频
            video_id = pixverse_image_to_video(img_id, args)

            # 获取生成结果
            generate_result, video_url = pixverse_get_result(video_id)

            # 生成成功
            if generate_result:
                # 下载视频
                if download_video(video_url, video_path):
                    end_time = round(time.time() - start_time, 2)
                    server_logger.info(f"[Pixverse] Finish Pixverse process in {end_time} seconds.")
                    return True

        return False
    else:
        time.sleep(30)
        return True
