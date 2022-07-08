from datetime import datetime

from blockchain import blockexplorer

from src.bitcoin import abuse, rpc, util
from src.database import abused_account_dao
from src.database.entity import AbusedAccount
from src.database.sqlalchemy.util import batch_insert

abused_account_set = set()


def init_abused_account_set():
    abused_addresses = abused_account_dao.select_all_addresses()
    for address in abused_addresses:
        abused_account_set.add(address.lower())
    print(f"恶意地址数据集初始化完成：{len(abused_account_set)}")
    pass


def init_abused_account_table():
    if abused_account_dao.count_all() == 0:
        items = abuse.parse_csv("dataset/bitcoin-abuse.csv")
        abused_accounts = [AbusedAccount(created_at=item.created_at, message=item.description, address=item.address, uploader=item.abuser) for item in items]
        batch_insert(abused_accounts, 2048)
    pass


def is_abused_account(address: str) -> bool:
    return abused_account_dao.exists_by_address(address)


def add_abused_account(address: str, message: str, abuser: str):
    abused_account = AbusedAccount(created_at=datetime.now(), message=message, address=address, uploader=abuser)
    abused_account_dao.insert_abused_account(abused_account)
    abused_account_set.add(address)
    pass


def get_abuse_messages(address: str):
    abused_accounts = abused_account_dao.select_by_address(address)
    return [{
        "message": item.message,
        "translatedMessage": item.message,
        "info": f'{item.uploader} 上传于 {item.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    } for item in abused_accounts]


def get_related_abused_accounts(address: str):
    target_address = blockexplorer.get_address(address)
    txids = [tx.hash for tx in target_address.transactions]
    result = list()
    txs = rpc.get_raw_transactions(txids)
    for tx in txs:
        outputs = util.get_tx_outputs(tx)
        address_iter = [item.payee for item in outputs]
        for item in address_iter:
            if item != address:
                messages = get_abuse_messages(item)
                if len(messages) > 0:
                    result.append({
                        "address": item,
                        "abuses": messages
                    })
    return result


# 初始化恶意账户数据表
init_abused_account_table()
# 初始化恶意地址集合提高查询速度（全部转换为小写）
init_abused_account_set()
