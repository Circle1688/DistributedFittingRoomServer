import subprocess
from converter.female_measurement_converter import female_converter
from converter.male_measurement_converter import male_converter
from plugin_server.utils import *


def start_ue():
    params = [UE_BAT_PATH, '-ForceRes', f"-ResX={str(UE_RES_X)}", f"-ResY={str(UE_RES_Y)}"]
    
    if UE_HEADLESS.lower() == 'true':
        params.append('-RenderOffScreen')

    proc = subprocess.Popen(params, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    server_logger.info(f"[UE] UE process has been started at {proc.pid}")
    time.sleep(1)
    return proc.pid


def convert_inputs(json_data):
    gender = json_data['user_details']['gender']
    real_world_measurements = json_data['user_details']['real_world_measurements']

    if gender.lower() == 'female':
        body_dimensions, body_dimension_lengths = female_converter(real_world_measurements)
    else:
        body_dimensions, body_dimension_lengths = male_converter(real_world_measurements)

    json_data['user_details']['body_dimensions'] = body_dimensions
    json_data['user_details']['body_dimension_lengths'] = body_dimension_lengths

    return json_data


def ue_process(ue_json_data):

    server_logger.info("[UE] Start UE process...")

    # 转换输入
    convert_json_data = convert_inputs(ue_json_data)

    # 启动一个独立进程
    pid = start_ue()

    # 连接
    while True:
        try:
            # 先试着连接到UE
            server_logger.info("[UE] Connect to ue...")

            response = requests.post(UE_URL, json=convert_json_data, timeout=2.0)
            break
        except requests.exceptions.Timeout:
            server_logger.info("[UE] Try again later...")
            time.sleep(1)

    server_logger.info("[UE] UE is online")

    start_time = time.time()

    server_logger.info("[UE] Start ue process...")

    rsp_json = response.json()

    images_folder = rsp_json['image']

    server_logger.info("[UE] Check finish tag...")

    while True:
        # 等待图片输出
        file_path = os.path.join(images_folder, "finish.tag")

        # 检查完成文件是否存在
        if os.path.isfile(file_path):
            server_logger.info("[UE] Found finish tag")
            end_time = round(time.time() - start_time, 2)
            server_logger.info(f"[UE] Finish UE process in {end_time} seconds.")
            break

    # 关闭ue
    kill_process_by_name(UE_EXE_NAME)

    return images_folder
