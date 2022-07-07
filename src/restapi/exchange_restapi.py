from src.restapi.restapi_decorator import restapi
from src.service import exchange_service


def setup_exchange_restapi(app):
    @app.route('/btc/getExchangeRates', methods=['GET', 'POST'])
    @restapi
    def get_exchange_rates():
        exchange_rates = exchange_service.get_exchange_rates()
        return {"exchangeRates": exchange_rates}
