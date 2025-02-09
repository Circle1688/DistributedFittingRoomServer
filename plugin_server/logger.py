import os
import logging
from logging.handlers import RotatingFileHandler

def logger_config(log_path, logging_name):
    """
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    """
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)

    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)

    # 获取文件日志句柄并设置日志级别，第二层过滤
    # 限制文件大小
    handler = RotatingFileHandler(f'./log/{log_path}', encoding='UTF-8', maxBytes=100 * 1024, backupCount=1)
    handler.setLevel(logging.INFO)

    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)

    return logger

# 日志
if not os.path.exists("./log"):
    os.mkdir("./log")

server_logger = logger_config(log_path='facefusion_server.log', logging_name='FaceFusionAPI')
