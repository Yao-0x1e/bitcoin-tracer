import os
import time
from collections import namedtuple
from typing import List

import requests
from enum import Enum

from src.config.app_config import app_ini as ai

api_token = ai.get('bitcoin', 'abuse_db_api_token')

CsvItem = namedtuple('CsvItem', ['id', 'address', 'abuse_type_id', 'abuse_type_other', 'abuser', 'description', 'from_country', 'from_country_code', 'created_at'])


class TimePeriod(Enum):
    day = '1d'
    month = '30d'
    forever = 'forever'
    pass


def download_csv(file: str, time_period: TimePeriod = TimePeriod.forever):
    assert not os.path.exists(file)
    assert time_period is not None

    url = "https://www.bitcoinabuse.com/api/download/%s?api_token=%s" % (time_period.value, api_token)
    print('正在下载：' + url)
    req = requests.get(url)
    with open(file, mode='wb') as f:
        f.write(req.content)
    pass


def parse_csv(file: str) -> List[CsvItem]:
    items = list()
    with open(file, mode='r', errors='ignore') as f:
        csv_lines = f.readlines()[1:]
        csv_lines = ''.join(csv_lines).split('.000000Z\n')
        for csv_line in csv_lines:
            if len(csv_line) >= 64:
                columns = csv_line.split(',', maxsplit=5)
                assert len(columns) == 6
                item_id = columns[0]
                address = columns[1]
                abuse_type_id = columns[2]
                abuse_type_other = columns[3]
                abuser = columns[4]
                columns = columns[5].rsplit(',', maxsplit=3)
                assert len(columns) == 4
                description = columns[0]
                from_country = columns[1]
                from_country_code = columns[2]
                created_at = time.strptime(columns[3].replace('T', ' '), "%Y-%m-%d %H:%M:%S")
                items.append(CsvItem(item_id, address, abuse_type_id, abuse_type_other, abuser, description, from_country, from_country_code, created_at))
    return items
