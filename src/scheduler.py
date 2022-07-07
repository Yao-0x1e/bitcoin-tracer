import time
from threading import Thread

import schedule

from src import app_context
from src.service import address_service, block_service, transaction_service


def job():
    block_service.synchronize_blocks(batch_size=64)
    app_context.cached_active_address_count_in_recent_hours = address_service.get_active_address_count_in_recent_hours(num_hours=24)
    app_context.cached_transaction_count_in_recent_hours = transaction_service.get_tx_count_in_recent_hours(num_hours=24)
    app_context.cached_risky_transactions = transaction_service.get_latest_risky_txs(block_count=50)
    app_context.cached_large_balance_transactions = transaction_service.get_latest_large_balance_txs(block_count=50, tx_count=300)
    pass


def setup_schedules():
    schedule.every(5).minutes.do(job)

    def run_schedules():
        while True:
            schedule.run_pending()
            time.sleep(1)

    Thread(target=run_schedules).start()
    pass
