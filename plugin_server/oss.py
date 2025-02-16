import oss2

from plugin_server.config import *
from plugin_server.logger import server_logger

auth = oss2.AuthV4(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

# 创建Bucket实例，指定存储空间的名称和Region信息。
bucket = oss2.Bucket(auth, END_POINT, BUCKET_NAME, region=REGION)


def upload_file_oss(file_path, upload_path):
    result = bucket.put_object_from_file(upload_path, file_path)
    if result.status == 200:
        server_logger.info("[OSS] File upload successfully.")
        return True
    else:
        server_logger.info("[OSS] File upload failed.")
        return False


def upload_obj_oss(file_obj, upload_path):
    result = bucket.put_object(upload_path, file_obj)
    if result.status == 200:
        server_logger.info("[OSS] Upload successfully.")
        return True
    else:
        server_logger.info("[OSS] Upload failed.")
        return False


def delete_obj_oss(file_path):
    result = bucket.delete_object(file_path)
    if result.status == 200:
        server_logger.info("[OSS] Delete successfully.")
        return True
    else:
        server_logger.info("[OSS] Delete failed.")
        return False


def get_files_oss(folder_prefix):
    files = []
    for obj in oss2.ObjectIteratorV2(bucket, prefix=folder_prefix):
        files.append((obj.key, obj.last_modified))
    # 按最后修改时间排序（从晚到早）
    files_sorted_by_time = sorted(files, key=lambda x: x[1], reverse=True)

    file_list = []
    for key, last_modified in files_sorted_by_time:
        file_list.append((get_full_url_oss(key), last_modified))

    return file_list


def get_full_url_oss(filename):
    return CDN + '/' + filename
