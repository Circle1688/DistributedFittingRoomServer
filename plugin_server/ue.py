import time
import subprocess
import requests

from plugin_server.config import *
from plugin_server.logger import server_logger
from plugin_server.utils import *


def ue_process(ue_json_data):
    start_time = time.time()
    # 先请求ue
    try:
        # 先试着连接到UE
        server_logger.info("[UE] Connect to ue...")
        response = requests.post(UE_URL, json=ue_json_data, timeout=2.0)
    except requests.exceptions.Timeout:
        # 如果连接不上UE
        server_logger.info("[UE] UE is offline")

        target_process_name = "FittingRoom.exe"

        # 先清理所有的残留进程 包括crash的
        kill_process_by_name(target_process_name)

        server_logger.info("[UE] Restart UE process...")
        # 启动一个独立进程，执行FittingRoom.exe程序，并指定creationflags参数
        proc = subprocess.Popen([target_process_name, f"-ResX={UE_RES_X}", f"-ResY={UE_RES_Y}"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

        # 等待进程启动完成
        while True:
            time.sleep(1)
            # 使用psutil检查进程的状态
            p = psutil.Process(proc.pid)
            if p.status() in [psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING]:
                server_logger.info("[UE] UE process has been started")
                break
            else:
                server_logger.info("[UE] UE process has not been started yet")

        # 等待ue启动完成
        time.sleep(2)

        # 重新连接
        while True:
            try:
                # 先试着连接到UE
                server_logger.info("[UE] Connect to ue...")
                response = requests.post(UE_URL, json=ue_json_data, timeout=2.0)
                break
            except requests.exceptions.Timeout:
                server_logger.info("[UE] Try again later...")
                time.sleep(1)

    server_logger.info("[UE] UE is online")
    server_logger.info("[UE] Start ue process...")

    rsp_json = response.json()

    images_folder = rsp_json['image']

    server_logger.info("[UE] Check finish tag...")
    while True:
        # 等待图片输出
        time.sleep(2)
        file_path = os.path.join(images_folder, "finish.tag")

        # 检查完成文件是否存在
        if os.path.isfile(file_path):
            server_logger.info("[UE] Found finish tag")
            end_time = round(time.time() - start_time, 2)
            server_logger.info(f"[UE] Finish UE process in {end_time} seconds.")
            break

    return images_folder
