from datetime import datetime

from src.bitcoin.rpc import BitcoinRPC
from src.database.block_dao import BlockDao
from src.database.sqlalchemy import Block, batch_insert


class BlockService:
    @staticmethod
    def sync_block_headers(batch_size: int):
        block_num = BlockDao.count_all()
        block_hash = BitcoinRPC.get_block_hash(block_num)
        latest_block_hash = BitcoinRPC.get_latest_block_hash()
        block_headers = list()
        while block_hash != latest_block_hash:
            block = BitcoinRPC.get_block(block_hash, True)
            block_num = block['height']
            block_time = datetime.fromtimestamp(block['time'])
            tx_count = block['nTx']
            block_headers.append(Block(no=block_num, hash=block_hash, timestamp=block_time, num_txs=tx_count))
            block_hash = block['nextblockhash']
            if len(block_headers) >= batch_size:
                batch_insert(block_headers, batch_size)
                block_headers.clear()
            block_num += 1
        if len(block_headers) > 0:
            batch_insert(block_headers, batch_size)
        pass
