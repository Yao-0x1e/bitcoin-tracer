from datetime import datetime
from typing import List

from sqlalchemy import and_, func

from src.database.entity import Block
from src.database.sqlalchemy.util import safe_query


def get_blocks_between_timestamps(start_time: datetime, end_time: datetime) -> List[Block]:
    return safe_query(lambda session: session.query(Block).filter(and_(Block.timestamp >= start_time, Block.timestamp < end_time)).all())


def count_all() -> int:
    return safe_query(lambda session: session.query(func.count(Block.no)).first()[0])
