import requests
from plugin_server.logger import server_logger
from plugin_server.config import *
from plugin_server.utils import *


def upscale_process(input_path, output_path):
    try:
        server_logger.info("[Upscale] Start upscale")
        request_data = {
            "input_path": os.path.abspath(input_path).replace('\\', '/'),
            "output_path": os.path.abspath(output_path).replace('\\', '/'),
        }
        # 请求Upscale
        resp = requests.post(UPSCALE_URL, json=request_data)

        if resp.status_code != 200:
            server_logger.exception(f"[Upscale] Failed. Error code: {resp.status_code}")
            return False

        server_logger.info("[Upscale] Successfully")
        return True

    except Exception as e:
        server_logger.exception(f"[Upscale] Exception {e}")

        return False
