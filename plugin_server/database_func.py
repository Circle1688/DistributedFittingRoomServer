from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from plugin_server.models import Base, TaskStorage

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/db_fittingroom?charset=utf8"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_db():
	db = Session()
	try:
		yield db
	finally:
		db.close()


def init_db():
	Base.metadata.create_all(engine)


init_db()

session = Session()
# 删除任务表中所有数据
session.query(TaskStorage).delete()
session.commit()
session.close()
