import time
from datetime import datetime
from typing import List

from src.bitcoin.bitcoin_rpc import BitcoinRPC
from src.database.block_dao import BlockDao


class AddressService:

    @staticmethod
    def get_latest_active_address_count(block_count: int) -> int:
        block_hash = BitcoinRPC.get_latest_block_hash()
        result = 0
        for _ in range(block_count):
            block = BitcoinRPC.get_block(block_hash)
            for tx in block['tx']:
                result += len(tx['vin']) + len(tx['vout'])
            block_hash = block['previousblockhash']
        return result

    @staticmethod
    def get_active_address_count(start_time: int, end_time: int) -> int:
        start_time -= 28800
        end_time -= 28800
        blocks = BlockDao.get_blocks_by_timestamp(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
        result = 0
        for item in blocks:
            block = BitcoinRPC.get_block(item.hash)
            for tx in block['tx']:
                result += len(tx['vin']) + len(tx['vout'])
        return result

    @staticmethod
    def get_active_address_count_in_recent_hours(num_hours: int) -> List[dict]:
        result = list()
        end_time = int(datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())
        end_time -= 28800
        start_time = end_time - 3600
        for _ in range(num_hours):
            address_count = AddressService.get_active_address_count(start_time, end_time)
            time_key = time.strftime("%H:%M", time.localtime(start_time + 28800))
            result.append({time_key: address_count})
            end_time -= 3600
            start_time -= 3600
        return list(reversed(result))
