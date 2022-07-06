from datetime import datetime

from blockchain import blockexplorer

from src.bitcoin.bitcoin_rpc import BitcoinRPC
from src.bitcoin.bitcoin_utils import BitcoinUtils
from src.bitcoin.bitcoin_abuse import parse_csv
from src.database.abused_account_dao import AbusedAccountDao
from src.database.sqlalchemy import AbusedAccount, batch_insert


class AbusedAccountService:
    @staticmethod
    def init_abused_accounts():
        if AbusedAccountDao.count_all() == 0:
            items = parse_csv("dataset/bitcoin-abuse.csv")
            abused_accounts = [AbusedAccount(created_at=item.created_at, message=item.description, address=item.address, uploader=item.abuser) for item in items]
            batch_insert(abused_accounts, 2048)
        pass

    @staticmethod
    def is_abused_account(address: str) -> bool:
        return AbusedAccountDao.exists_by_address(address)

    @staticmethod
    def add_abused_account(address: str, message: str, abuser: str):
        abused_account = AbusedAccount(created_at=datetime.now(), message=message, address=address, uploader=abuser)
        AbusedAccountDao.insert_abused_account(abused_account)
        pass

    @staticmethod
    def get_abuse_messages(address: str):
        abused_accounts = AbusedAccountDao.select_by_address(address)
        return [{
            "message": item.message,
            "translatedMessage": item.message,
            "info": f'{item.uploader} 上传于 {item.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
        } for item in abused_accounts]

    @staticmethod
    def get_related_abused_accounts(address: str):
        target_address = blockexplorer.get_address(address)
        txids = [tx.hash for tx in target_address.transactions]
        result = list()
        for txid in txids:
            tx = BitcoinRPC.get_raw_transaction(txid)
            outputs = BitcoinUtils.get_tx_outputs(tx)
            address_iter = [item.payee for item in outputs]
            for item in address_iter:
                if item != address:
                    messages = AbusedAccountService.get_abuse_messages(item)
                    if len(messages) > 0:
                        result.append({
                            "address": item,
                            "abuses": messages
                        })
        return result
