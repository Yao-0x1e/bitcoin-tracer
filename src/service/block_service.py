from datetime import datetime

from src.bitcoin import rpc
from src.database import block_dao
from src.database.entity import Block
from src.database.sqlalchemy.util import batch_insert


def synchronize_blocks(batch_size: int):
    block_height = block_dao.count_all()
    block_hash = rpc.get_block_hash(block_height)
    latest_block_hash = rpc.get_latest_block_hash()
    blocks = list()
    while block_hash != latest_block_hash:
        block_header = rpc.get_block_header(block_hash)
        block_height = block_header['height']
        block_time = datetime.fromtimestamp(block_header['time'])
        tx_count = block_header['nTx']
        blocks.append(Block(height=block_height, hash=block_hash, mined_at=block_time, num_txs=tx_count))

        if len(blocks) >= batch_size:
            batch_insert(blocks, batch_size)
            blocks.clear()
        block_hash = block_header['nextblockhash']
    if len(blocks) > 0:
        batch_insert(blocks, batch_size)
    pass
