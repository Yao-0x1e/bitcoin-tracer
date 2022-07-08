from queue import Queue
from threading import BoundedSemaphore
from typing import List

import ujson
from bitcoinrpc.authproxy import AuthServiceProxy

from src.config.app_config import app_ini as ai
from src.config.redis_config import redis_conn

proxy_url = "http://%s:%s@%s:%d" % (
    ai.get('bitcoin', 'rpc_user'),
    ai.get('bitcoin', 'rpc_password'),
    ai.get('bitcoin', 'rpc_host'),
    ai.getint('bitcoin', 'rpc_port')
)
proxy_timeout = ai.getint('bitcoin', 'rpc_timeout')
proxy_qsize = ai.getint('bitcoin', 'proxy_queue_size')
proxy_queue = Queue()
mutex = BoundedSemaphore(proxy_qsize)


def init_proxy_queue():
    for _ in range(proxy_qsize):
        proxy = AuthServiceProxy(proxy_url, timeout=proxy_timeout)
        proxy_queue.put(proxy)
    pass


# noinspection PyBroadException
def execute(target):
    mutex.acquire()
    proxy = proxy_queue.get()
    try:
        return target(proxy)
    except Exception as ex:
        proxy = AuthServiceProxy(proxy_url, timeout=proxy_timeout)
        raise ex
    finally:
        proxy_queue.put(proxy)
        mutex.release()
    pass


def get_raw_transaction(txid: str) -> dict:
    redis_key = 'rawtransactions:' + txid
    redis_val = redis_conn.get(redis_key)
    if redis_val is not None:
        return ujson.loads(redis_val)
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
