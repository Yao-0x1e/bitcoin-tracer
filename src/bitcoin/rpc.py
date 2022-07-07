from queue import Queue
from threading import BoundedSemaphore
from typing import List

from bitcoinrpc.authproxy import AuthServiceProxy

from src.app_config import app_ini as ai

proxy_qsize = 4
proxy_queue = Queue()
mutex = BoundedSemaphore(proxy_qsize)


def execute(target):
    mutex.acquire()
    proxy = proxy_queue.get()
    try:
        return target(proxy)
    finally:
        proxy_queue.put(proxy)
        mutex.release()
    pass


def init_proxy_queue():
    proxy_url = "http://%s:%s@%s:%d" % (
        ai.get('bitcoinRPC', 'user'),
        ai.get('bitcoinRPC', 'password'),
        ai.get('bitcoinRPC', 'host'),
        ai.getint('bitcoinRPC', 'port')
    )
    for _ in range(proxy_qsize):
        proxy = AuthServiceProxy(proxy_url)
        proxy_queue.put(proxy)
    pass


def get_raw_transaction(txid: str) -> dict:
    return execute(lambda proxy: proxy.getrawtransaction(txid, 1))


def get_raw_transactions(txids: List[str]) -> List[dict]:
    return execute(lambda proxy: proxy.batch_([['getrawtransaction', txid, 1] for txid in txids]))


def get_block_count() -> int:
    return execute(lambda proxy: proxy.getblockcount())


def get_blockchain_info() -> dict:
    return execute(lambda proxy: proxy.getblockchaininfo())


def get_latest_block_hash() -> str:
    return execute(lambda proxy: proxy.getbestblockhash())


def get_block_hash(block_num: int) -> str:
    return execute(lambda proxy: proxy.getblockhash(block_num))


def get_block_hashes(block_nums: List[int]) -> List[dict]:
    return execute(lambda proxy: proxy.batch_([['getblockhash', block_num] for block_num in block_nums]))


def get_block(block_hash: str, only_txids: bool = False) -> dict:
    verbosity = 1 if only_txids else 2
    return execute(lambda proxy: proxy.getblock(block_hash, verbosity))


def get_blocks(block_hashes: List[str], only_txids: bool = False) -> List[dict]:
    verbosity = 1 if only_txids else 2
    return execute(lambda proxy: proxy.batch_([['getblock', block_hash, verbosity] for block_hash in block_hashes]))


def get_block_header(block_hash: str) -> dict:
    return execute(lambda proxy: proxy.getblockheader(block_hash))


def get_block_headers(block_hashes: List[str]) -> List[dict]:
    return execute(lambda proxy: proxy.batch_([['getblockheader', block_hash] for block_hash in block_hashes]))


init_proxy_queue()
