from plugin_server.utils import *
from plugin_server.config import TRY_ON_FOLDER

from virtual_try_on.kling import process as kling_process


def get_cloth_image(request_data):
    gender = request_data['user_details']['gender']
    apparel_details = request_data['apparel_details']
    brand = apparel_details['brand']
    clothing_name = apparel_details['item_id']
    color = apparel_details['color']
    cloth_image_path = os.path.join(TRY_ON_FOLDER, f'{brand}/{gender}/{clothing_name}_{color}.png')

    return cloth_image_path


def virtual_try_on(render_mode, human_image_path, request_data):
    cloth_image_path = get_cloth_image(request_data)
    if render_mode == '2D_Kling':
        return kling_process(human_image_path, cloth_image_path)

    return False
