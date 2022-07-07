from blockchain import exchangerates


def get_exchange_rates() -> dict:
    ticker = exchangerates.get_ticker()
    result = dict()
    for key in ticker:
        result[key] = ticker[key].p15min
    return result
