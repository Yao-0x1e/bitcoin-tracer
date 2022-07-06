from typing import List

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

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Block(Base):
    __tablename__ = 'block'
    no = Column(INT, primary_key=True)
    hash = Column(VARCHAR(128), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    num_txs = Column(INT, nullable=False)
    pass


class AbusedAccount(Base):
    __tablename__ = 'abused_account'
    no = Column(INT, primary_key=True, autoincrement=True)
    address = Column(VARCHAR(128), index=True)
    message = Column(TEXT, default='')
    uploader = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    pass


# 根据基类的 Metadata 自动创建表
Base.metadata.create_all(engine)


# noinspection PyBroadException
def safe_update(target):
    session = Session()
    try:
        res = target(session)
        session.commit()
        return res
    except Exception:
        session.rollback()
    finally:
        session.close()


# noinspection PyBroadException
def safe_query(target):
    session = Session()
    try:
        res = target(session)
        return res
    finally:
        session.close()


def batch_insert(items: List[Base], batch_size: int):
    def target(session: Session):
        start_index, end_index = 0, batch_size
        while start_index < len(items):
            session.add_all(items[start_index:end_index])
            session.commit()
            start_index += batch_size
            end_index += batch_size

    safe_update(target)
    pass
