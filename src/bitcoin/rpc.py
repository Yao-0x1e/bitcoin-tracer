from threading import Lock
from typing import List

from bitcoinrpc.authproxy import AuthServiceProxy

from src.app_config import app_ini as ai

proxy = AuthServiceProxy("http://%s:%s@%s:%d" % (
    ai.get('bitcoinRPC', 'user'),
    ai.get('bitcoinRPC', 'password'),
    ai.get('bitcoinRPC', 'host'),
    ai.getint('bitcoinRPC', 'port')
))
mutex = Lock()


def concurrent(target):
    def wrapper(*args, **kwargs):
        try:
            mutex.acquire()
            return target(*args, **kwargs)
        finally:
            mutex.release()
        pass

    return wrapper


@concurrent
def get_raw_transaction(txid: str) -> dict:
    return proxy.getrawtransaction(txid, 1)


@concurrent
def get_raw_transactions(txids: List[str]) -> List[dict]:
    return proxy.batch_([['getrawtransaction', txid, 1] for txid in txids])


@concurrent
def get_block_count() -> int:
    return proxy.getblockcount()


@concurrent
def get_blockchain_info() -> dict:
    return proxy.getblockchaininfo()


@concurrent
def get_latest_block_hash() -> str:
    return proxy.getbestblockhash()


@concurrent
def get_block_hash(block_num: int) -> str:
    return proxy.getblockhash(block_num)


@concurrent
def get_block_hashes(block_nums: List[int]) -> List[dict]:
    return proxy.batch_([['getblockhash', block_num] for block_num in block_nums])


@concurrent
def get_block(block_hash: str, only_txids: bool = False) -> dict:
    verbosity = 1 if only_txids else 2
    return proxy.getblock(block_hash, verbosity)


@concurrent
def get_blocks(block_hashes: List[str], only_txids: bool = False) -> List[dict]:
    verbosity = 1 if only_txids else 2
    return proxy.batch_([['getblock', block_hash, verbosity] for block_hash in block_hashes])


def get_block_header(block_hash: str) -> dict:
    return proxy.getblockheader(block_hash)


@concurrent
def get_block_headers(block_hashes: List[str]) -> List[dict]:
    return proxy.batch_([['getblockheader', block_hash] for block_hash in block_hashes])
