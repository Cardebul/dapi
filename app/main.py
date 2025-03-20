from flask import Flask

from app.analytics import analytics_api
from app.base_api_views import base_api

app = Flask(__name__)
app.register_blueprint(base_api)
app.register_blueprint(analytics_api)