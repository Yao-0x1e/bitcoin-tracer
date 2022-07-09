import time
from threading import Thread

import schedule

from src.service import block_service, address_service, transaction_service


def leak_exceptions(target):
    try:
        target()
    except Exception as ex:
        print(ex)
    pass


def setup_schedules():
    schedule.every(10).minutes.do(lambda: leak_exceptions(lambda: block_service.synchronize_blocks(batch_size=64)))
    schedule.every(60).minutes.do(lambda: leak_exceptions(lambda: address_service.get_active_address_counts_in_recent_hours(num_hours=24)))
    schedule.every(60).minutes.do(lambda: leak_exceptions(lambda: transaction_service.get_tx_counts_in_recent_hours(num_hours=24)))
    schedule.every(10).minutes.do(lambda: leak_exceptions(lambda: transaction_service.get_latest_risky_txs(block_count=50)))
    schedule.every(10).minutes.do(lambda: leak_exceptions(lambda: transaction_service.get_latest_large_balance_txs(block_count=50, tx_count=300)))

    def run_schedules():
        print("定时任务已开始执行！")
        schedule.run_all(delay_seconds=10 * 60)
        while True:
            schedule.run_pending()
            time.sleep(15)

    Thread(target=run_schedules).start()
    pass
