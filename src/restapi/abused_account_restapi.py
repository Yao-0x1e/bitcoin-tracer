from flask import request

from src.restapi.restapi_decorator import restapi
from src.service import abused_account_service


def setup_abused_account_restapi(app):
    @app.route('/btc/isMaliciousAccount', methods=['GET', 'POST'])
    @restapi
    def is_malicious_account():
        address = request.values.get('address')
        messages = abused_account_service.get_abuse_messages(address)
        return {
            "isMalicious": len(messages) > 0,
            "abuses": messages
        }

    @app.route('/btc/getRelevantMaliciousAccounts', methods=['GET', 'POST'])
    @restapi
    def get_related_abused_accounts():
        address = request.values.get('address')
        accounts = abused_account_service.get_related_abused_accounts(address)
        return {"maliciousAccounts": accounts}

    @app.route('/btc/addMaliciousAccount', methods=['GET', 'POST'])
    @restapi
    def add_malicious_account():
        address = request.values.get('address')
        message = request.values.get('message')
        abuser = request.values.get('abuser')
        abused_account_service.add_abused_account(address, message, abuser)
        return {}
