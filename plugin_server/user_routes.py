from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from plugin_server.models import *
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session
from plugin_server.schemas import *
from plugin_server.auth import create_token, get_current_user_id


router = APIRouter()

# 创建账户
@router.post('/register')
async def register_user(user_data: UserData, db: Session = Depends(get_db)):
	email = user_data.email
	full_name = user_data.full_name
	date_of_birth = user_data.date_of_birth
	ethnicity = user_data.ethnicity
	gender = user_data.gender

	if email == "":
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email can not be empty")

	# 查询用户
	db_user = db.query(User).filter(User.email == email).first()

	if db_user is not None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account {email} has already created")

	# 创建新用户
	new_user = User()

	new_user.email = email

	# 用户信息
	new_user.user_info = UserInfo(email=email, full_name=full_name, date_of_birth=date_of_birth, ethnicity=ethnicity, gender=gender)

	# 用户数据
	new_user.user_detail = UserDetailBase()

	# token
	new_user.token = TokenStorage(token="")

	db.add(new_user)
	try:
		db.commit()
		db.refresh(new_user)
	except IntegrityError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

	return {"message": f"Account {email} has been created"}


@router.post('/login')
async def login_user(user_data: UserData, db: Session = Depends(get_db)):
	email = user_data.email

	# 查询用户
	db_user = db.query(User).filter(User.email == email).first()

	if db_user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	user_id = db_user.id
	new_token = create_token(user_id)

	# 存入token
	db.query(TokenStorage).filter(TokenStorage.user_id == user_id).update({"token": new_token})
	db.commit()

	return {"token": new_token}


# 获取用户的账户信息
@router.get('/get_user_info')
async def get_user_info(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
	userinfo = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

	if userinfo is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	result = userinfo.__dict__
	result.pop('user_id')
	result.pop('id')

	return result

# 更新用户的账户信息
@router.post('/update_user_info')
async def update_user_info(user_data: UserData, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
	userinfo = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

	if userinfo is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	# 更新字段
	userinfo.full_name = user_data.full_name
	userinfo.date_of_birth = user_data.date_of_birth
	userinfo.ethnicity = user_data.ethnicity
	userinfo.gender = user_data.gender

	db.commit()
	db.refresh(userinfo)

	return {"message": "user info updated successfully"}
