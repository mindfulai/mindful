# imports
import os
import pendulum
import json

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

# get the folder where this file runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create app
app = Flask(__name__)
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


@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)


@app.route('/twitter_auth')
def twitter_auth():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)

    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok

    screen_name = resp.json()['screen_name']
    app.logger.info('%s logged in successfully', screen_name)
    # app.logger.info('%s logged in successfully', resp.json())

    resp_user_account = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    # WON'T use account activity api
    # FOR The account activity api has limitation on accounts subscribed, and we don't really need the realtime data.
    # Instead query twitter user's tweets and mentions is just enough.

    # WON'T use statuses/home_timeline.json
    # FOR the response include tweets from followings
    # resp = twitter.get("statuses/home_timeline.json")

    # WILL use statuses/user_timeline.json
    # FOR the 20 most recent tweets for the authenticating user.
    #
    # TODO:
    #   * tweets_today(days=1)
    resp = twitter.get("statuses/user_timeline.json?screen_name=" + screen_name)
    assert resp.ok

    app.logger.info('%s logged in successfully', resp.json())

    resp_user_timeline = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    # WILL use statuses/mentions_timeline.json
    # FOR the 20 most recent mentions for the authenticating user.
    #
    # TODO:
    #   * mentions_today(days=1)
    resp = twitter.get("statuses/mentions_timeline.json?screen_name=" + screen_name)
    assert resp.ok

    app.logger.info('%s logged in successfully', resp.json())

    resp_mentions_timeline = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    return render_template('twitter.html', screen_name=screen_name, resp_user_account=resp_user_account,
                           entries=entries, resp_user_timeline=resp_user_timeline,
                           resp_mentions_timeline=resp_mentions_timeline)

@app.route('/twitter/timeline')
def twitter_timeline():
    """
    将 timeline 存入
    """
    screen_name = 'linxuedong'
    # TODO: 查找数据库中的 tweet 找到最大 tweet_id，通过 since_id 载入他与 tweet_id 的文章

    resp = twitter.get("statuses/user_timeline.json?screen_name=" + screen_name)
    assert resp.ok

    timeline = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    # 存入数据库
    for tweet in resp.json():
        user = tweet['user']['screen_name']
        tweet_id = tweet['id']
        created_at = pendulum.parse(tweet['created_at'], strict=False)
        t = models.Tweet(tweet_json=json.dumps(tweet), created_at=created_at,
                         user=user, api_url=resp.url, tweet_id=tweet_id)
        db.session.add(t)
        db.session.commit()

    return jsonify({'tweets': timeline})

@app.route('/facebook_auth')
def facebook_auth():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))

    return render_template('facebook.html')

@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database."""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Flaskr)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')


if __name__ == '__main__':
    app.run()
