from fastapi import APIRouter, Depends, HTTPException, status

from plugin_server.models import *
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session
from plugin_server.schemas import *
from plugin_server.auth import get_current_user_id

router = APIRouter()

@router.post('/update_user_details')
async def update_user_details(modify_data: UserDetail, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
	face_shape = modify_data.face_shape
	skin_tone = modify_data.skin_tone
	body_dimensions = modify_data.body_dimensions
	real_world_measurements = modify_data.real_world_measurements
	hair_style = modify_data.hair_style
	hair_color = modify_data.hair_color

	# 查找user detail
	db_user_detail = db.query(UserDetailBase).filter(UserDetailBase.user_id == user_id).first()

	# 更新字段
	db_user_detail.face_shape = face_shape
	db_user_detail.skin_tone = skin_tone
	db_user_detail.hair_style = hair_style
	db_user_detail.hair_color = hair_color
	db_user_detail.body_dimensions = body_dimensions
	db_user_detail.real_world_measurements = real_world_measurements

	db.commit()
	db.refresh(db_user_detail)

	return {"message": f"User details updated successfully"}

@router.get('/get_user_details')
async def get_user_details(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
	# 获取user details
	db_user_detail = db.query(UserDetailBase).filter(UserDetailBase.user_id == user_id).first()

	result = db_user_detail.__dict__
	result.pop('user_id')
	result.pop('id')

	return result
