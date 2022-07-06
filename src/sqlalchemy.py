from sqlalchemy import create_engine, Column, BINARY, TIMESTAMP, INT, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app_config import app_ini as ai

# 创建 SQLAlchemy Engine
engine = create_engine("mysql+pymysql://%s:%s@%s:%d/%s" % (
    ai.get('mysql', 'user'),
    ai.get('mysql', 'password'),
    ai.get('mysql', 'host'),
    ai.getint('mysql', 'port'),
    ai.get('mysql', 'schema')
), pool_size=4, echo=True, encoding='utf8mb4')

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Block(Base):
    __tablename__ = 'block'
    no = Column(INT, primary_key=True)
    hash = Column(BINARY(256), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    num_txs = Column(INT, nullable=False)
    pass


class AbusedAccount(Base):
    __tablename__ = 'abused_address'
    address = Column(BINARY(256), primary_key=True)
    message = Column(VARCHAR(65535), default='')
    uploader = Column(VARCHAR(255), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    pass


# 根据基类的 Metadata 自动创建表
Base.metadata.create_all(engine)
