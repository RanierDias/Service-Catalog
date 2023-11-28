from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()


def run_app():
    app = Flask(__name__)
    domains = os.getenv('DOMAINS').split(', ')

    if os.getenv('DEV'):
        CORS(app, origins=["*"], methods=["GET", "OPTIONS"])
        Talisman(app)
    else:
        CORS(app, origins=domains, methods=[
             "GET", "POST", "PATCH", "DELETE", "OPTIONS"])
        Talisman(app)

    from .controllers import product_bp, user_bp

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
