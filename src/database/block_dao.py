from datetime import datetime
from typing import List

from sqlalchemy import and_, func

from src.database.entity import Block
from src.database.sqlalchemy.util import safe_query


def get_blocks_between_timestamps(start_time: datetime, end_time: datetime) -> List[Block]:
    return safe_query(lambda session: session.query(Block).filter(and_(Block.mined_at >= start_time, Block.mined_at < end_time)).all())


def count_all() -> int:
    return safe_query(lambda session: session.query(func.count(Block.height)).first()[0])
