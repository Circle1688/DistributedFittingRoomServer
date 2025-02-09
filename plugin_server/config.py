import configparser

config = configparser.ConfigParser()
config.read('config.ini')

USER_DATA_DIR = config['default']['user_data_dir']
SERVER_HOST = config['default']['server_host']
REDIS_HOST = config['default']['redis_host']

UE_URL = config['worker']['ue_url']
UE_RES_X = config['worker']['ue_res_x']
UE_RES_Y = config['worker']['ue_res_y']
FACEFUSION_URL = config['worker']['facefusion_url']
PIXVERSE_API_KEY = config['worker']['pixverse_apiKey']
