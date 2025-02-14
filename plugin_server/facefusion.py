import time
import requests

from plugin_server.config import *
from plugin_server.logger import server_logger
from plugin_server.utils import *


def stop_facefusion_task():
	try:
		# 请求facefusion
		resp = requests.get(FACEFUSION_URL + '_stop')

		if resp.status_code != 200:
			server_logger.exception(f"[FaceFusion stop failed] {resp.status_code}")
			return False

		server_logger.exception("[FaceFusion] stop task successfully")
		return True

	except Exception as e:
		server_logger.exception(f"[FaceFusion stop exception] {e}")

		return False


def facefusion_image_internal(source_image_path, target_image_path, image_output_path):
	start_time = time.time()
	server_logger.info("[FaceFusionImage] Start facefusion image process...")
	try:
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(target_image_path),
			"output_path": os.path.abspath(image_output_path)
		}
		try:
			resp = requests.post(FACEFUSION_URL, json=request_data, timeout=15)

			if resp.status_code != 200:
				server_logger.exception(f"[Image generation failed] {resp.status_code}")
				return False, None

		except requests.exceptions.Timeout:
			if not stop_facefusion_task():
				return False, None

		# 压缩
		img = Image.open(image_output_path)

		file_name, file_extension = image_output_path.rsplit('.', 1)
		jpg_path = f"{file_name}.jpg"

		# 以指定质量保存压缩后的结果
		img.save(jpg_path, quality=100)

		# 移除png原图
		os.remove(image_output_path)

		end_time = round(time.time() - start_time, 2)
		server_logger.info(f"[FaceFusionImage] Finish facefusion image process in {end_time} seconds.")

		return True, jpg_path
	except Exception as e:
		server_logger.exception(f"[Image generation exception] {e}")

		return False, None


def facefusion_image(task_id, source_image_path, images_folder, output_path, image_options):
	quality = image_options['quality']
	thumbnail_width = image_options['thumbnail_width']

	target_image_paths = find_png_files(images_folder)
	for i, target_image_path in enumerate(target_image_paths):

		image_output_path = os.path.join(output_path, task_id + f"-{i + 1}" + ".png")

		server_logger.info(f"FaceFusion process image... {i + 1} of {len(target_image_paths)}")

		result, image_output_path = facefusion_image_internal(source_image_path, target_image_path, image_output_path)

		# 生成成功
		if result:
			# 生成缩略图
			server_logger.info(f"Generate thumbnail...")
			compress_image(image_output_path, quality, thumbnail_width)
		else:
			return False

	return True


def facefusion_video(task_id, source_image_path, video_path, output_path):
	start_time = time.time()
	server_logger.info("[FaceFusionVideo] Start facefusion video process...")
	try:
		video_output_path = os.path.join(output_path, task_id + ".mp4")
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(video_path),
			"output_path": os.path.abspath(video_output_path)
		}
		try:
			resp = requests.post(FACEFUSION_URL, json=request_data, timeout=40)

			if resp.status_code != 200:
				server_logger.exception(f"[Video generation failed] {resp.status_code}")
				return False

		except requests.exceptions.Timeout:
			if not stop_facefusion_task():
				return False

		end_time = round(time.time() - start_time, 2)
		server_logger.info(f"[FaceFusionVideo] Finish facefusion video process in {end_time} seconds.")
		return True

	except Exception as e:
		server_logger.exception(f"[Video generation exception] {e}")

		return False
