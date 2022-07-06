from flask import Flask
from flask_cors import CORS

from src.service.abused_account_service import AbusedAccountService

app = Flask(__name__)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    AbusedAccountService.init_abused_accounts()
    # app.run(host="0.0.0.0", port=5000, debug=True)
    pass
