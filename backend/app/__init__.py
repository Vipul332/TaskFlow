from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import init_extensions
from .routes import register_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        supports_credentials=True
    )

    init_extensions(app)

    register_routes(app)

    return app