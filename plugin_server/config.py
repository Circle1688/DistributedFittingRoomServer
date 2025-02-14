import configparser

config = configparser.ConfigParser()
config.read('config.ini')

USER_DATA_DIR = config['default']['user_data_dir']
SERVER_HOST = config['default']['server_host']
REDIS_HOST = config['default']['redis_host']

UE_URL = config['ue']['url']
UE_RES_X = config['ue']['res_x']
UE_RES_Y = config['ue']['res_y']
UE_HEADLESS = config['ue']['headless']
UE_EXE_NAME = config['ue']['exe_name']
UE_BAT_PATH = config['ue']['bat_path']


FACEFUSION_URL = config['worker']['facefusion_url']
PIXVERSE_API_KEY = config['worker']['pixverse_apiKey']
UPSCALE_URL = config['worker']['upscale_url']
