from flask import Flask
from flask_cors import CORS
from gevent import pywsgi

from src.config.app_config import app_ini as ai
from src.restapi.abused_account_restapi import setup_abused_account_restapi
from src.restapi.address_restapi import setup_address_restapi
from src.restapi.exchange_restapi import setup_exchange_restapi
from src.restapi.transaction_restapi import setup_transaction_restapi

app = Flask(__name__)
CORS(app, supports_credentials=True)


def setup_all_restapi():
    setup_abused_account_restapi(app)
    setup_address_restapi(app)
    setup_transaction_restapi(app)
    setup_exchange_restapi(app)
    pass


def run_flask_server():
    flask_host = ai.get('flask', 'host')
    flask_port = ai.getint('flask', 'port')
    app.run(host=flask_host, port=flask_port, debug=False, threaded=True)
    # pywsgi.WSGIServer((flask_host, flask_port), app).serve_forever()
    pass


if __name__ == '__main__':
    # 初始化所有 API
    setup_all_restapi()
    # 启动 Web 服务
    run_flask_server()
    pass
