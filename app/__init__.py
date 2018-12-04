from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask import send_file, send_from_directory

import pathlib

front_end_path = pathlib.Path(__file__).parent.parent / 'mindful/dist'

app = Flask(__name__, static_folder=str(front_end_path / 'static'))
app.config.from_object('config')

CORS(app)

db = SQLAlchemy(app)

# 登录
login_manager = LoginManager()
login_manager.login_view = 'facebook.login'

login_manager.init_app(app)

from app.views import facebook_blueprint, twitter_blueprint

app.register_blueprint(twitter_blueprint, url_prefix="/login")
app.register_blueprint(facebook_blueprint, url_prefix="/login")


@app.route('/')
def index():
    return send_file(str(front_end_path / 'index.html'))
