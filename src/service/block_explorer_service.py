import pickle
from typing import List

from blockchain import blockexplorer
from blockchain.blockexplorer import UnspentOutput, Address

from src.config.redis_config import cacheable


@cacheable(prefix='blockexplorer:address', serializer=pickle.dumps, deserializer=pickle.loads)
def get_address(address: str) -> Address:
    return blockexplorer.get_address(address)


@cacheable(prefix='blockexplorer:unspent-outputs', serializer=pickle.dumps, deserializer=pickle.loads)
def get_unspent_outputs(address: str) -> List[UnspentOutput]:
    # noinspection PyTypeChecker
    return blockexplorer.get_unspent_outputs(address)
