from datetime import datetime
from typing import List

from sqlalchemy import and_, func

from src.database.sqlalchemy import Session, Block, safe_query, safe_update


class BlockDao:
    @staticmethod
    def get_blocks_by_timestamp(start_time: datetime, end_time: datetime) -> List[Block]:
        def target(session: Session):
            return session.query(Block).filter(and_(Block.timestamp >= start_time, Block.timestamp < end_time)).all()

        return safe_query(target)

    @staticmethod
    def count_all() -> int:
        def target(session: Session):
            return session.query(func.count(Block.no)).first()[0]

        return safe_query(target)

