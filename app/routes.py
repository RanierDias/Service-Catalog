from .controllers import product_bp, user_bp
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources=r"/*",
     origins=['https://catalogo-virtual-ranierdias.vercel.app/'])


app.register_blueprint(product_bp, url_prefix='/products')

app.register_blueprint(user_bp, url_prefix='/user')
