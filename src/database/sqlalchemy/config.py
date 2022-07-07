from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app_config import app_ini as ai

# 创建 SQLAlchemy Engine
engine = create_engine("mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8mb4" % (
    ai.get('mysql', 'user'),
    ai.get('mysql', 'password'),
    ai.get('mysql', 'host'),
    ai.getint('mysql', 'port'),
    ai.get('mysql', 'schema')
), pool_size=4, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
