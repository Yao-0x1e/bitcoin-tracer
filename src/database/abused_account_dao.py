from typing import List

from sqlalchemy import func

from src.database.entity import AbusedAccount
from src.database.sqlalchemy.util import safe_query, safe_update


def count_all() -> int:
    return safe_query(lambda session: session.query(func.count(AbusedAccount.no)).first()[0])


def insert_abused_account(abused_account: AbusedAccount):
    return safe_update(lambda session: session.add(abused_account))


def select_by_address(address: str) -> List[AbusedAccount]:
    return safe_query(lambda session: session.query(AbusedAccount).filter(AbusedAccount.address == address).all())


def exists_by_address(address: str) -> AbusedAccount:
    return safe_query(lambda session: session.query(func.count(AbusedAccount.no)).filter(AbusedAccount.address == address).first()[0] > 0)


def select_in_addresses(addresses: List[str]) -> List[AbusedAccount]:
    # noinspection PyUnresolvedReferences
    return safe_query(lambda session: session.query(AbusedAccount).filter(AbusedAccount.address.in_(addresses)).all())


def select_all() -> List[AbusedAccount]:
    # noinspection PyUnresolvedReferences
    return safe_query(lambda session: session.query(AbusedAccount).all())


def select_all_addresses() -> List[str]:
    # noinspection PyUnresolvedReferences
    result = safe_query(lambda session: session.query(AbusedAccount.address).distinct(AbusedAccount.address).all())
    return [item[0] for item in result]
