import glob
import shutil

import psutil
from PIL import Image
import os


def find_png_files(directory):
    png_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    return png_files


def get_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append({"filename": file, "filepath": os.path.join(root, file)})
    return file_list


def get_sorted_files(directory):
    # 获取目录下的所有文件
    files = glob.glob(os.path.join(directory, '*'))

    # 按修改时间排序（最新的在前）
    files.sort(key=os.path.getmtime, reverse=True)

    # 只返回文件名
    return [os.path.basename(file) for file in files]


def clear_folder(directory):
    # 检查目录是否存在
    if not os.path.exists(directory):
        return

    # 遍历目录并删除所有内容
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            # 如果是文件或符号链接，直接删除
            os.unlink(item_path)

        elif os.path.isdir(item_path):
            # 如果是子目录，递归删除整个目录
            shutil.rmtree(item_path)


def compress_image(source_path, quality, thumbnail_width):
    with Image.open(source_path) as img:
        # 计算缩略图的高度，保持图片的原始宽高比
        width, height = img.size
        thumbnail_height = int((thumbnail_width / width) * height)

        # 调整图片大小为缩略图尺寸
        img.thumbnail((thumbnail_width, thumbnail_height))

        file_name, file_extension = source_path.rsplit('.', 1)
        thumbnail_path = f"{file_name}_thumbnail.jpg"

        # 以指定质量保存缩略图
        img.save(thumbnail_path, quality=quality)


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                proc = psutil.Process(proc.info['pid'])
                proc.terminate()  # 先尝试发送SIGTERM信号
                try:
                    proc.wait(timeout=3)  # 等待3秒，看进程是否结束
                except psutil.TimeoutExpired:
                    print(f"Process {process_name} PID: {proc.info['pid']} No response to SIGTERM signal, try sending SIGKILL signal")
                    proc.kill()  # 发送SIGKILL信号强制结束进程
                    proc.wait(timeout=3)  # 再次等待进程结束
                print(f"Process{process_name} PID: {proc.info['pid']} has been ended")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Error while ending process: {e}")
