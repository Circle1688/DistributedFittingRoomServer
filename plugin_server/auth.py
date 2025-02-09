import time

import jwt
from fastapi import Depends, HTTPException, Header, status
from plugin_server.database_func import get_db
from sqlalchemy.orm import Session
from plugin_server.models import *

SECRET_KEY = "fittingroom"
ALGORITHM = "HS256"

def create_token(user_id: int):
	to_encode = {"user_id": user_id, "timestamp": int(time.time() * 1000)}
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

async def get_current_user_id(authorization: str = Header(None), db: Session = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Invalid authorization credentials",
		headers={"WWW-Authenticate": "Bearer"}
	)
	if authorization and authorization.startswith("Bearer"):
		token = authorization.split(" ")[1]
	else:
		raise credentials_exception
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id: int = payload.get("user_id")
		if user_id is None:
			raise credentials_exception
	except jwt.PyJWTError:
		raise credentials_exception

	# 查询用户
	db_token = db.query(TokenStorage).filter(TokenStorage.user_id == user_id).first()
	if db_token is None:
		raise credentials_exception

	# 验证token
	if token == db_token.token:
		return user_id
	else:
		raise credentials_exception
