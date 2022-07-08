from blockchain import exchangerates

from src.config.redis_config import cacheable


@cacheable(prefix='exchangerates', ex=15 * 60)
def get_exchange_rates() -> dict:
    ticker = exchangerates.get_ticker()
    result = dict()
    for key in ticker:
        result[key] = ticker[key].p15min
    return result
