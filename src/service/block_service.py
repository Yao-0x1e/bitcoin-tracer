from datetime import datetime
import time
from threading import Thread

import schedule
import ujson

from src.config.app_config import app_ini as ai
from src.bitcoin import rpc
from src.config.redis_config import redis_conn
from src.database import block_dao
from src.database.entity import Block
from src.database.sqlalchemy_utils import batch_insert
from src.service import address_service, transaction_service


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


def setup_schedules():
    def scheduled_task():
        synchronize_blocks(batch_size=64)
        redis_conn.set('statistic:active-address-count-in-recent-hours', ujson.dumps(address_service.get_active_address_count_in_recent_hours(num_hours=24)))
        redis_conn.set('statistic:transaction-count-in-recent-hours', ujson.dumps(transaction_service.get_tx_count_in_recent_hours(num_hours=24)))
        redis_conn.set('statistic:risky-transactions', ujson.dumps(transaction_service.get_latest_risky_txs(block_count=50)))
        redis_conn.set('statistic:large-balance-transactions', ujson.dumps(transaction_service.get_latest_large_balance_txs(block_count=50, tx_count=300)))
        pass

    interval = ai.getint('schedule', 'interval')
    schedule.every(interval).seconds.do(scheduled_task)

    def run_schedules():
        schedule.run_all(delay_seconds=interval)
        while True:
            schedule.run_pending()
            time.sleep(15)

    Thread(target=run_schedules).start()
    pass


# 开始定时任务
setup_schedules()
