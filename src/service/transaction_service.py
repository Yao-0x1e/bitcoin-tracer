import time
from datetime import datetime
from queue import Queue, PriorityQueue
from typing import List

from blockchain import blockexplorer

from src.bitcoin import utils, rpc
from src.config.redis_config import cacheable, redis_conn
from src.database import block_dao
from src.service import abused_account_service, block_explorer_service
from src.service.abused_account_service import is_abused_account, has_abused_accounts_in


def is_risky_tx(tx: dict) -> bool:
    redis_key = "transaction:is-risky:" + tx['txid']
    if redis_conn.exists(redis_key):
        return True
    outputs = utils.get_tx_outputs(tx)
    # inputs = utils.get_tx_inputs(tx)
    # related_address_set = {vout.payee for vout in outputs}.union({vin.payer for vin in inputs})
    related_address_set = {vout.payee for vout in outputs}
    is_risky = has_abused_accounts_in(related_address_set)
    if is_risky:
        redis_conn.set(redis_key, '', ex=3600)
    return is_risky


@cacheable(prefix='transaction:tx-inputs')
def get_tx_inputs(txid: str) -> List[dict]:
    tx = rpc.get_raw_transaction(txid)
    inputs = utils.get_tx_inputs(tx)
    return [{
        "address": item.payer,
        "balance": item.balance,
        "isMalicious": abused_account_service.is_abused_account(item.payer)
    } for item in inputs]


@cacheable(prefix='transaction:tx-outputs', ex=3600)
def get_tx_outputs(txid: str) -> List[dict]:
    tx = rpc.get_raw_transaction(txid)
    outputs = utils.get_tx_outputs(tx)
    return [{
        "address": item[0],
        "balance": item[1],
        "isMalicious": abused_account_service.is_abused_account(item.payee)
    } for item in outputs]


@cacheable(prefix='transaction:input-txs')
def get_input_txs(txid: str) -> List[dict]:
    tx = rpc.get_raw_transaction(txid)
    result = list()
    if not utils.is_coinbase_tx(tx):
        spent_txids = [item['txid'] for item in tx['vin']]
        spent_txs = rpc.get_raw_transactions(spent_txids)
        for spent_tx in spent_txs:
            result.append({
                "txid": spent_tx['txid'],
                "isRisky": is_risky_tx(spent_tx),
            })
    return result


@cacheable(prefix='transaction:input-tx-tree', ex=3600)
def get_input_tx_tree(root_txid: str, depth: int, risky_only: bool) -> dict:
    assert depth >= 1
    root_tx = {
        "name": root_txid,
        "isRisky": is_risky_tx(rpc.get_raw_transaction(root_txid)),
    }
    tx_queue = Queue()
    tx_queue.put(root_tx)
    for _ in range(depth - 1):
        qsize = tx_queue.qsize()
        for _ in range(qsize):
            node = tx_queue.get()
            children = list()
            input_txs = get_input_txs(node['name'])
            for tx in input_txs:
                tx['name'] = tx.pop('txid')
                children.append(tx)
                if risky_only and not tx['isRisky']:
                    continue
                tx_queue.put(tx)
            if len(children) > 0:
                node['children'] = children
    return root_tx


@cacheable(prefix='transaction:account-txs', ex=3600)
def get_all_txs_of_account(address: str) -> List[dict]:
    target_address = block_explorer_service.get_address(address)
    result = list()
    for tx in target_address.transactions:
        is_risky = False
        for item in tx.inputs + tx.outputs:
            if is_abused_account(item.address):
                is_risky = True
                break
        result.append({
            "txid": tx.hash,
            "isRisky": is_risky
        })
    return result


@cacheable(prefix='transaction:account-payer-txs', ex=3600)
def get_payer_txs_of_account(address: str) -> List[dict]:
    target_address = block_explorer_service.get_address(address)
    result = list()
    for tx in target_address.transactions:
        inputs = ((item.address, item.value) for item in tx.inputs)
        inputs = list(filter(lambda item: item[0] == address, inputs))
        if len(inputs) > 0:
            total_balance = 0
            for item in inputs:
                total_balance += item[1]
            total_balance /= 1e8
            related_address_set = {item.address for item in tx.inputs + tx.outputs}
            is_risky = has_abused_accounts_in(related_address_set)
            result.append({
                "txid": tx.hash,
                "balance": total_balance,
                "isRisky": is_risky
            })
    return result


@cacheable(prefix='transaction:account-payee-txs', ex=3600)
def get_payee_txs_of_account(address: str) -> List[dict]:
    target_address = block_explorer_service.get_address(address)
    result = list()
    for tx in target_address.transactions:
        outputs = ((item.address, item.value) for item in tx.outputs)
        outputs = list(filter(lambda item: item[0] == address, outputs))
        if len(outputs) > 0:
            total_balance = 0
            for item in outputs:
                total_balance += item[1]
            total_balance /= 1e8
            related_address_set = {item.address for item in tx.inputs + tx.outputs}
            is_risky = has_abused_accounts_in(related_address_set)
            result.append({
                "txid": tx.hash,
                "balance": total_balance,
                "isRisky": is_risky
            })
    return result


@cacheable(prefix='transaction:unspent_outputs')
def get_unspent_tx_outputs_of_account(address: str) -> List[dict]:
    # noinspection PyTypeChecker
    outputs = block_explorer_service.get_unspent_outputs(address)
    return [{
        "txid": item.tx_hash,
        "vout": item.tx_output_n
    } for item in outputs]


@cacheable(prefix='transaction:latest-txs', ex=600)
def get_latest_txs(block_count: int) -> List[dict]:
    result = list()
    block_hash = rpc.get_latest_block_hash()
    for _ in range(block_count):
        block = rpc.get_block(block_hash)
        block_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block['time']))
        for tx in block['tx']:
            result.append({
                "txid": tx['txid'],
                "isRisky": is_risky_tx(tx),
                "balance": utils.get_total_balance(tx),
                "time": block_time
            })
    result = sorted(result, reverse=True, key=lambda item: item['balance'])
    risky_txs = filter(lambda item: item['isRisky'], result)
    non_risky_txs = filter(lambda item: not item['isRisky'], result)
    return list(risky_txs) + list(non_risky_txs)


@cacheable(prefix='transaction:latest-risky-txs', ex=1800)
def get_latest_risky_txs(block_count: int) -> List[dict]:
    txs = list()
    block_hash = rpc.get_latest_block_hash()
    for _ in range(block_count):
        block = rpc.get_block(block_hash)
        block_txs = block['tx']
        block_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block['time']))
        for tx in block_txs:
            tx['blocktime'] = block_time
        txs += block_txs
        block_hash = block['previousblockhash']
    result = list()
    for tx in txs:
        if is_risky_tx(tx):
            block_time = tx['blocktime']
            result.append({
                "txid": tx['txid'],
                "balance": utils.get_total_balance(tx),
                "time": block_time
            })
    return list(sorted(result, key=lambda x: x['balance'], reverse=True))


@cacheable(prefix='transaction:latest-tx-count', ex=600)
def get_latest_tx_count(block_count: int) -> int:
    block_hash = rpc.get_latest_block_hash()
    result = 0
    for _ in range(block_count):
        block_header = rpc.get_block_header(block_hash)
        result += block_header['nTx']
        block_hash = block_header['previousblockhash']
    return result


@cacheable(prefix='transaction:count-between-times')
def get_tx_count(start_time: int, end_time: int) -> int:
    start_time -= 28800
    end_time -= 28800
    blocks = block_dao.get_blocks_between_timestamps(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
    result = 0
    for item in blocks:
        result += item.num_txs
    return result


@cacheable(prefix='transaction:count-in-recent-hours', ex=2 * 3600)
def get_tx_counts_in_recent_hours(num_hours: int) -> List[dict]:
    result = list()
    end_time = int(datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())
    print(end_time)
    end_time -= 28800
    start_time = end_time - 3600
    for _ in range(num_hours):
        tx_count = get_tx_count(start_time, end_time)
        time_key = time.strftime("%H:%M", time.localtime(end_time + 28800))
        result.append({time_key: tx_count})
        end_time -= 3600
        start_time -= 3600
    return list(reversed(result))


@cacheable(prefix='transaction:large-balance-txs', ex=1800)
def get_latest_large_balance_txs(block_count: int, tx_count: int) -> List[dict]:
    txs = list()
    block_hash = rpc.get_latest_block_hash()
    for _ in range(block_count):
        block = rpc.get_block(block_hash)
        block_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block['time']))
        block_txs = block['tx']
        for tx in block_txs:
            tx['blocktime'] = block_time
        txs += block_txs
        block_hash = block['previousblockhash']
    priority_queue = PriorityQueue()
    min_balance = 0
    for tx in txs:
        total_balance = utils.get_total_balance(tx)
        if total_balance >= min_balance:
            block_time = tx['blocktime']
            item = (total_balance, tx['txid'], block_time)
            priority_queue.put(item)
            qsize = priority_queue.qsize()
            if qsize > tx_count:
                item = priority_queue.get()
                min_balance = item[0]
    result = list()
    while not priority_queue.empty():
        item = priority_queue.get()
        result.append({
            "txid": item[1],
            "balance": item[0],
            "time": item[2],
        })
    return list(reversed(result))


@cacheable(prefix='transaction:large-balance-tx-count', ex=600)
def get_latest_large_balance_tx_count(block_count: int, min_balance: float) -> int:
    block_hash = rpc.get_latest_block_hash()
    result = 0
    for _ in range(block_count):
        block = rpc.get_block(block_hash)
        for tx in block['tx']:
            total_balance = utils.get_total_balance(tx)
            if total_balance >= min_balance:
                result += 1
        block_hash = block['previousblockhash']
    return result
