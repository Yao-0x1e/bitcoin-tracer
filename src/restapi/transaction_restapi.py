from flask import request

from src import app_context
from src.restapi.restapi_decorator import restapi
from src.service import transaction_service


def setup_transaction_restapi(app):
    @app.route('/btc/getLatestTransactions', methods=['GET', 'POST'])
    @restapi
    def get_latest_transactions():
        block_count = int(request.values.get('blockCount'))
        txs = transaction_service.get_latest_txs(block_count)
        return {"txs": txs}

    @app.route('/btc/getTransactionOutputs', methods=['GET', 'POST'])
    @restapi
    def get_transaction_outputs():
        txid = request.values.get('txid')
        outputs = transaction_service.get_tx_outputs(txid)
        return {"outputs": outputs}

    @app.route('/btc/getTransactionInputs', methods=['GET', 'POST'])
    @restapi
    def get_transaction_inputs():
        txid = request.values.get('txid')
        inputs = transaction_service.get_tx_inputs(txid)
        return {"inputs": inputs}

    @app.route('/btc/getInputTransactions', methods=['GET', 'POST'])
    @restapi
    def get_input_transactions():
        txid = request.values.get('txid')
        txs = transaction_service.get_input_txs(txid)
        return {"txs": txs}

    @app.route('/btc/getAllTransactionsOfAccount', methods=['GET', 'POST'])
    @restapi
    def get_all_transactions_of_account():
        address = request.values.get('address')
        txs = transaction_service.get_all_txs_of_account(address)
        return {"txs": txs}

    @app.route('/btc/getPayerTransactionsOfAccount', methods=['GET', 'POST'])
    @restapi
    def get_payer_transactions_of_account():
        address = request.values.get('address')
        txids = transaction_service.get_payer_txs_of_account(address)
        return {"txs": txids}

    @app.route('/btc/getPayeeTransactionsOfAccount', methods=['GET', 'POST'])
    @restapi
    def get_payee_transactions_of_account():
        address = request.values.get('address')
        txs = transaction_service.get_payee_txs_of_account(address)
        return {"txs": txs}

    @app.route('/btc/getUnspentTransactionOutputsOfAccount', methods=['GET', 'POST'])
    @restapi
    def get_unspent_transactions_of_account():
        address = request.values.get('address')
        tx_outputs = transaction_service.get_unspent_tx_outputs_of_account(address)
        return {"txOutputs": tx_outputs}

    @app.route('/btc/getLatestLargeBalanceTransactions', methods=['GET', 'POST'])
    @restapi
    def get_latest_large_balance_transactions():
        block_count = int(request.values.get('blockCount'))
        tx_count = int(request.values.get('transactionCount'))
        txs = transaction_service.get_latest_large_balance_txs(block_count, tx_count)
        return {"txs": txs}

    @app.route('/btc/getCachedLargeBalanceTransactions', methods=['GET', 'POST'])
    @restapi
    def get_cached_large_balance_transactions():
        txs = app_context.cached_large_balance_transactions
        return {"txs": txs}

    @app.route('/btc/getLatestRiskyTransactions', methods=['GET', 'POST'])
    @restapi
    def get_latest_risky_transactions():
        block_count = int(request.values.get('blockCount'))
        txs = transaction_service.get_latest_risky_txs(block_count)
        return {"txs": txs}

    @app.route('/btc/getCachedRiskyTransactions', methods=['GET', 'POST'])
    @restapi
    def get_cached_risky_transactions():
        txs = app_context.cached_risky_transactions
        return {"txs": txs}

    @app.route('/btc/getLatestTransactionCount', methods=['GET', 'POST'])
    @restapi
    def get_latest_transaction_count():
        block_count = int(request.values.get('blockCount'))
        tx_count = transaction_service.get_latest_tx_count(block_count)
        return {"txCount": tx_count}

    @app.route('/btc/getTransactionCount', methods=['GET', 'POST'])
    @restapi
    def get_transaction_count():
        start_time = int(request.values.get('startTime'))
        end_time = int(request.values.get('endTime'))
        tx_count = transaction_service.get_tx_count(start_time, end_time)
        return {"txCount": tx_count}

    @app.route('/btc/getLatestLargeBalanceTransactionCount', methods=['GET', 'POST'])
    @restapi
    def get_latest_large_balance_transaction_count():
        block_count = int(request.values.get('blockCount'))
        min_balance = float(request.values.get('minBalance'))
        tx_count = transaction_service.get_latest_large_balance_tx_count(block_count, min_balance)
        return {"txCount": tx_count}

    @app.route('/btc/getTransactionCountInRecentHours', methods=['GET', 'POST'])
    @restapi
    def get_transaction_count_in_recent_hours():
        tx_counts = app_context.cached_transaction_count_in_recent_hours
        return {"txCounts": tx_counts}

    @app.route('/btc/getInputTransactionTree', methods=['GET', 'POST'])
    @restapi
    def get_input_transaction_tree():
        root_txid = request.values.get('txid')
        depth = int(request.values.get('depth'))
        risky_only = int(request.values.get('riskyOnly'))
        assert risky_only == 0 or risky_only == 1
        tree = transaction_service.get_input_tx_tree(root_txid, depth, risky_only == 1)
        return {"tree": tree}
