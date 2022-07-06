import time
from threading import Thread

import schedule

from src import app_context
from src.service.address_service import AddressService
from src.service.block_service import BlockService
from src.service.transaction_service import TransactionService


class ScheduleService:
    @staticmethod
    def setup_schedules():
        def refresh_cache():
            app_context.cached_active_address_count_in_recent_hours = AddressService.get_active_address_count_in_recent_hours(num_hours=24)
            app_context.cached_transaction_count_in_recent_hours = TransactionService.get_tx_count_in_recent_hours(num_hours=24)
            app_context.cached_risky_transactions = TransactionService.get_latest_risky_txs(block_count=50)
            app_context.cached_large_balance_transactions = TransactionService.get_latest_large_balance_txs(block_count=50, tx_count=300)
            pass

        schedule.every(5).minutes.do(lambda: BlockService.synchronize_blocks(batch_size=64))
        schedule.every(2).minutes.do(refresh_cache)

        def run_schedules():
            while True:
                schedule.run_pending()
                time.sleep(1)

        Thread(target=run_schedules).start()
        pass
