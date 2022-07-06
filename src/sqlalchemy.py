from sqlalchemy import create_engine, Column, TIMESTAMP, INT, VARCHAR, BLOB, TEXT
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


class Block(Base):
    __tablename__ = 'block'
    no = Column(INT, primary_key=True)
    hash = Column(VARCHAR(128), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    num_txs = Column(INT, nullable=False)
    pass


class AbusedAccount(Base):
    __tablename__ = 'abused_address'
    no = Column(INT, primary_key=True, autoincrement=True)
    address = Column(VARCHAR(128), index=True)
    message = Column(TEXT, default='')
    uploader = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    pass


# 根据基类的 Metadata 自动创建表
Base.metadata.create_all(engine)
