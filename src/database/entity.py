from sqlalchemy import Column, TIMESTAMP, INT, VARCHAR, TEXT

from src.config.sqlalchemy_config import engine, Base


class Block(Base):
    __tablename__ = 'block'
    height = Column(INT, primary_key=True, autoincrement=False)
    hash = Column(VARCHAR(128), nullable=False)
    mined_at = Column(TIMESTAMP, nullable=False, index=True)
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
