from pydantic import BaseModel
from typing import Optional, List


class UserData(BaseModel):
	email: Optional[str] = None
	full_name: Optional[str] = None
	date_of_birth: Optional[int] = None
	ethnicity: Optional[str] = None
	gender: Optional[str] = None


class FaceFusionRequestUserId(BaseModel):
	user_id: int
	ue_json_data: dict


class UserDetail(BaseModel):
	face_shape: Optional[str] = None
	skin_tone: Optional[int] = None
	body_dimensions: Optional[str] = None
	real_world_measurements: Optional[str] = None
	hair_style: Optional[str] = None
	hair_color: Optional[str] = None


class ApparelDetail(BaseModel):
	brand: Optional[str] = None
	item_id: Optional[str] = None
	color: Optional[str] = None
	size: Optional[str] = None
	size2: Optional[str] = None


class GenUserDetail(BaseModel):
	face_shape: str
	skin_tone: int
	pose: str
	body_dimensions: List[dict]
	body_dimension_lengths: List[dict]
	hairstyle: str
	hair_color: str
	camera_view: str
	view_mode: int
	expression: str
	background_color_hex: str
	gender: str


class ImageOptions(BaseModel):
	quality: int
	thumbnail_width: int


class VideoOptions(BaseModel):
	video_live: bool
	duration: int
	negative_prompt: str
	prompt: str
	seed: int


class TaskOptions(BaseModel):
	vip: bool
	limit: int


class GenerateRequest(BaseModel):
	user_details: GenUserDetail
	apparel_details: ApparelDetail
	image_options: ImageOptions
	task_options: TaskOptions


class VideoGenerateRequest(BaseModel):
	user_details: GenUserDetail
	apparel_details: ApparelDetail
	video_options: VideoOptions
	task_options: TaskOptions


class ClothesRequest(BaseModel):
	url: str
	brand: str
	name: str


class TaskRequest(BaseModel):
	user_id: int
	task_id: str
	status: str


class UpscaleRequest(BaseModel):
	video_url: str
	task_options: TaskOptions
