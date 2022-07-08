import time
from datetime import datetime
from typing import List

import ujson

from src.bitcoin import rpc
from src.config.redis_config import redis_conn
from src.database import block_dao


def get_latest_active_address_count(block_count: int) -> int:
    block_hash = rpc.get_latest_block_hash()
    result = 0
    for _ in range(block_count):
        block = rpc.get_block(block_hash)
        for tx in block['tx']:
            result += len(tx['vin']) + len(tx['vout'])
        block_hash = block['previousblockhash']
    return result


def get_active_address_count(start_time: int, end_time: int) -> int:
    start_time -= 28800
    end_time -= 28800
    blocks = block_dao.get_blocks_between_timestamps(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
    result = 0
    block_hashes = [item.hash for item in blocks]
    blocks = rpc.get_blocks(block_hashes)
    for block in blocks:
        for tx in block['tx']:
            result += len(tx['vin']) + len(tx['vout'])
    return result


def get_active_address_count_in_recent_hours(num_hours: int) -> List[dict]:
    result = list()
    end_time = int(datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())
    end_time -= 28800
    start_time = end_time - 3600
    for _ in range(num_hours):
        address_count = get_active_address_count(start_time, end_time)
        time_key = time.strftime("%H:%M", time.localtime(end_time + 28800))
        result.append({time_key: address_count})
        end_time -= 3600
        start_time -= 3600
    return list(reversed(result))


def get_cached_active_address_count_in_recent_hours():
    json_str = redis_conn.get('statistic:active-address-count-in-recent-hours')
    return ujson.loads(json_str) if json_str is not None else []
