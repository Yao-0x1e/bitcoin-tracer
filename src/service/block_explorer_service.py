from typing import List

from blockchain import blockexplorer
from blockchain.blockexplorer import Address, UnspentOutput

from src.config.redis_config import cacheable


@cacheable(prefix='blockexplorer-address', ex=3600)
def get_address_info(address: str) -> Address:
    return blockexplorer.get_address(address)


@cacheable(prefix='blockexplorer-unspent_outputs', ex=3600)
def get_unspent_outputs(address: str) -> List[UnspentOutput]:
    return blockexplorer.get_unspent_outputs((address,))
