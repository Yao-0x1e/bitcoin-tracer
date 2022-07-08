from flask import request


from src.restapi.restapi_decorator import restapi
from src.service import address_service


def setup_address_restapi(app):
    @app.route('/btc/getLatestActiveAddressCount', methods=['GET', 'POST'])
    @restapi
    def get_latest_active_address_count():
        block_count = int(request.values.get('blockCount'))
        address_count = address_service.get_latest_active_address_count(block_count)
        return {"addressCount": address_count}

    @app.route('/btc/getActiveAddressCountInRecentHours', methods=['GET', 'POST'])
    @restapi
    def get_active_address_count_in_recent_hours():
        address_counts = address_service.get_cached_active_address_count_in_recent_hours
        return {"addressCounts": address_counts}

    @app.route('/btc/getActiveAddressCount', methods=['GET', 'POST'])
    @restapi
    def get_active_address_count():
        start_time = int(request.values.get('startTime'))
        end_time = int(request.values.get('endTime'))
        address_count = address_service.get_active_address_count(start_time, end_time)
        return {"addressCount": address_count}
