# imports
import pendulum
import json

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from sqlalchemy.orm.exc import NoResultFound

from flask_cors import CORS


# create app
app = Flask(__name__)
CORS(app)

# load the instance config
app.config.from_pyfile('config.py')

# Twitter
twitter_blueprint = make_twitter_blueprint(
    api_key="devnDViKMhTY4J5AwVKW7NewW",
    api_secret="92kwOgTnMiFNGP1bXNvaLCOLSEIiX6WYSPYDohEWIAnsDceGja",
)
app.register_blueprint(twitter_blueprint, url_prefix="/login")
# Facebook
facebook_blueprint = make_facebook_blueprint(
    client_id="176320989922581",
    client_secret="bfbf2231584f211669debf63467e58e9",
)
app.register_blueprint(facebook_blueprint, url_prefix="/login")
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models
