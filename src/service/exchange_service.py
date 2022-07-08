import ujson
from blockchain import exchangerates

from src.config.redis_config import redis_conn


def get_exchange_rates() -> dict:
    json_str = redis_conn.get('exchange:rates')
    if json_str is not None:
        return ujson.loads(json_str)

    ticker = exchangerates.get_ticker()
    result = dict()
    for key in ticker:
        result[key] = ticker[key].p15min
    # 缓存并设置过期时间为15分钟
    redis_conn.set('exchange:rates', ujson.dumps(result), ex=15 * 60)
    return result
