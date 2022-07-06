from bitcoinrpc.authproxy import AuthServiceProxy

from src.app_config import app_ini as ai

proxy = AuthServiceProxy("http://%s:%s@%s:%d" % (
    ai.get('bitcoinRPC', 'user'),
    ai.get('bitcoinRPC', 'password'),
    ai.get('bitcoinRPC', 'host'),
    ai.getint('bitcoinRPC', 'port')
))


class BitcoinRPC:
    @staticmethod
    def get_raw_transaction(txid: str) -> dict:
        return proxy.getrawtransaction(txid, 1)

    @staticmethod
    def get_block_count() -> int:
        return proxy.getblockcount()

    @staticmethod
    def get_blockchain_info() -> dict:
        return proxy.getblockchaininfo()

    @staticmethod
    def get_latest_block_hash() -> str:
        return proxy.getbestblockhash()

    @staticmethod
    def get_block_hash(block_num: int) -> str:
        return proxy.getblockhash(block_num)

    @staticmethod
    def get_block(block_hash: str, only_txids: bool = False) -> dict:
        verbosity = 1 if only_txids else 2
        return proxy.getblock(block_hash, verbosity)

    @staticmethod
    def get_block_header(block_hash: str) -> dict:
        return proxy.getblockheader(block_hash)
