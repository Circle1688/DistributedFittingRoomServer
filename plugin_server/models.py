from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)

	email = Column(String(255))
	user_info = relationship("UserInfo", uselist=False, back_populates="user", cascade="all, delete-orphan")
	user_detail = relationship("UserDetailBase", uselist=False, back_populates="user", cascade="all, delete-orphan")
	token = relationship("TokenStorage", uselist=False, back_populates="user", cascade="all, delete-orphan")


class UserInfo(Base):
	__tablename__ = 'user_info'
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'), unique=True)

	email = Column(String(255))

	full_name = Column(String(255))
	date_of_birth = Column(Integer)
	ethnicity = Column(String(120))
	gender = Column(String(80))

	user = relationship("User", back_populates="user_info")


class UserDetailBase(Base):
	__tablename__ = 'user_detail'

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'), unique=True)

	face_shape = Column(String(80), default="")
	skin_tone = Column(Integer, default=0)
	hair_style = Column(String(80), default="")
	hair_color = Column(String(80), default="")
	body_dimensions = Column(Text, default="")
	real_world_measurements = Column(Text, default="")

	user = relationship("User", back_populates="user_detail")


class TokenStorage(Base):
	__tablename__ = 'token_storage'
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'), unique=True)

	token = Column(String(255))

	user = relationship("User", back_populates="token")


class Clothes(Base):
	__tablename__ = 'clothes'

	id = Column(Integer, primary_key=True, index=True)
	url = Column(String(255))
	brand = Column(String(80))
	gender = Column(String(80))
	name = Column(String(80))
	colors = Column(JSON)
	colors_hex = Column(JSON)
	sizes = Column(JSON)


class TaskStorage(Base):
	__tablename__ = 'task_storage'
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))

	task_id = Column(String(50), nullable=False)
	status = Column(String(50), nullable=False)


class Gallery(Base):
	__tablename__ = 'gallery'
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))

	source_url = Column(String(255))
	thumbnail_url = Column(String(255))
	last_modified = Column(Integer)
