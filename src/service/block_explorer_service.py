from typing import List

import ujson
from blockchain import blockexplorer
from blockchain.blockexplorer import Address, UnspentOutput

from src.config.redis_config import redis_conn


def get_address_info(address: str) -> Address:
    redis_key = 'blockexplorer-address-info:' + address
    redis_val = redis_conn.get(redis_key)
    if redis_val is not None:
        target_address = ujson.loads(redis_val)
    else:
        target_address = blockexplorer.get_address(address)
        redis_conn.set(redis_key, ujson.dumps(target_address), ex=6 * 3600)
    return target_address


def get_unspent_outputs(address: str) -> List[UnspentOutput]:
    redis_key = 'blockexplorer-unspent-outputs:' + address
    redis_val = redis_conn.get(redis_key)
    if redis_val is not None:
        unspent_outputs = ujson.loads(redis_val)
    else:
        unspent_outputs = blockexplorer.get_unspent_outputs((address,))
        redis_conn.set(redis_key, ujson.dumps(unspent_outputs), ex=6 * 3600)
    return unspent_outputs
