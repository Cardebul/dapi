import os

from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache

load_dotenv()


class AppConfig:
    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('DB_HOST')
    pg_port = os.getenv('DB_PORT')
    pg_db = os.getenv('POSTGRES_DB')

    debug = False if os.getenv('DEBUG') != 'True' else True

    cache_config = {
        "DEBUG": debug,
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300
    }


app = Flask(__name__)

app.config.from_mapping(AppConfig.cache_config)
cache = Cache(app)