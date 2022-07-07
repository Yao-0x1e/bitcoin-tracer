from typing import List

from src.database.sqlalchemy.config import Session, Base


def safe_update(target):
    session = Session()
    try:
        res = target(session)
        session.commit()
        return res
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()


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
