from flask import Flask
from flask_cors import CORS

from src.service.schedule_service import ScheduleService

app = Flask(__name__)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    ScheduleService.setup_schedules()
    app.run(host="0.0.0.0", port=5000, debug=True)
    pass
