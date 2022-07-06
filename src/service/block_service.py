from datetime import datetime

from src.bitcoin.bitcoin_rpc import BitcoinRPC
from src.database.block_dao import BlockDao
from src.database.sqlalchemy import Block, batch_insert


class BlockService:
    @staticmethod
    def synchronize_blocks(batch_size: int):
        block_num = BlockDao.count_all()
        block_hash = BitcoinRPC.get_block_hash(block_num)
        latest_block_hash = BitcoinRPC.get_latest_block_hash()
        blocks = list()
        while block_hash != latest_block_hash:
            block = BitcoinRPC.get_block(block_hash, True)
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
