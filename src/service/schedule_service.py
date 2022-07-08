import time
from threading import Thread

import schedule

from src.service import block_service, address_service


def setup_schedules():
    schedule.every(10).minutes.do(lambda: block_service.synchronize_blocks(batch_size=64))
    schedule.every(10).minutes.do(lambda: address_service.get_active_address_counts_in_recent_hours(num_hours=24))

    # TODO: 异常处理
    def run_schedules():
        print("定时任务已开始执行！")
        schedule.run_all(delay_seconds=10 * 60)
        while True:
            schedule.run_pending()
            time.sleep(15)

    Thread(target=run_schedules).start()
    pass
