from .controllers import product_bp, user_bp
from flask import Flask


app = Flask(__name__)


app.register_blueprint(product_bp, url_prefix='/products')

app.register_blueprint(user_bp, url_prefix='/user')
