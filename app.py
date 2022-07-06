from flask import Flask
from flask_cors import CORS

from src.bitcoin_abuse import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    parse_csv("dataset/bitcoin-abuse.csv")
    pass
