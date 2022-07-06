from typing import List

from sqlalchemy import func

from src.database.sqlalchemy import AbusedAccount, Session, safe_update, safe_query


class AbusedAccountDao:
    @staticmethod
    def count_all() -> int:
        def target(session: Session):
            return session.query(func.count(AbusedAccount.no)).first()[0]

        return safe_query(target)

    @staticmethod
    def insert_abused_account(abused_account: AbusedAccount):
        def target(session: Session):
            session.add(abused_account)

        safe_update(target)
        pass

    @staticmethod
    def select_by_address(address: str) -> List[AbusedAccount]:
        def target(session: Session):
            return session.query(AbusedAccount).filter(AbusedAccount.address == address).all()

        return safe_query(target)

    @staticmethod
    def exists_by_address(address: str) -> AbusedAccount:
        def target(session: Session):
            return session.query(func.count(AbusedAccount.no)).filter(AbusedAccount.address == address).first()[0] > 0

        return safe_query(target)

    @staticmethod
    def select_in_addresses(addresses: List[str]) -> List[AbusedAccount]:
        # noinspection PyUnresolvedReferences
        def target(session: Session):
            return session.query(AbusedAccount).filter(AbusedAccount.address.in_(addresses)).all()

        return safe_query(target)
