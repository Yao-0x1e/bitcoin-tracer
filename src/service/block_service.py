from datetime import datetime

from src.bitcoin import rpc
from src.database import block_dao
from src.database.entity import Block
from src.database.sqlalchemy.util import batch_insert


def synchronize_blocks(batch_size: int):
    block_num = block_dao.count_all()
    block_hash = rpc.get_block_hash(block_num)
    latest_block_hash = rpc.get_latest_block_hash()
    blocks = list()
    while block_hash != latest_block_hash:
        block = rpc.get_block(block_hash, True)
        block_num = block['height']
        block_time = datetime.fromtimestamp(block['time'])
        tx_count = block['nTx']
        blocks.append(Block(no=block_num, hash=block_hash, timestamp=block_time, num_txs=tx_count))
        block_hash = block['nextblockhash']
        if len(blocks) >= batch_size:
            batch_insert(blocks, batch_size)
            blocks.clear()
        block_num += 1
    if len(blocks) > 0:
        batch_insert(blocks, batch_size)
    pass
