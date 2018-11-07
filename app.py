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

    # 查找创建用户
    screen_name = resp.json()['screen_name']

    try:
        user = db.session.query(models.User).filter_by(
            username=screen_name).one()
    except:
        user = models.User(username=screen_name)
        db.session.add(user)
        db.session.commit()

    session['twitter_screen_name'] = user.username

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


def get_user_last_tweet_or_mention(user, csl):
    """获取数据库中最后的 tweet 或 mention
    args:
        user: 访问用户 object
        csl: 需要查找的 Tweet 或者 TweetMention
    retrun:
        数据库中最新的 tweet 或 mention
    """
    return db.session.query(csl).filter_by(user=user).order_by(
        csl.tweet_id.desc()).first()


def get_twitter_path(last_article, screen_name, article_type):
    """需要访问的路径
    args:
        last_tweet_or_mention: 数据库中最新的推文
        screen_name: 当前用户 twtter 用户名
        article_type: 是 twitter 还是 mention
    retrun:
        访问的 twitter API 路径

    TODO: 从什么时间开始获取 tweets
    """
    if article_type == 'tweet':
        api = 'statuses/user_timeline.json'
    elif article_type == 'mention':
        api = 'statuses/mentions_timeline.json'
    if last_article:
        max_tweet_id = last_article.tweet_id
        path = "{}?screen_name={}&since_id={}".format(
            api, screen_name, max_tweet_id)
    else:
        path = "{}?screen_name={}".format(api, screen_name)
    return path


def save_twitter_data(resp, user, csl):
    """存储 twitter 获取的数据到数据库
    args:
        resp: twitter API response
        user: 当前用户 object
    """
    for tweet in resp.json():
        tweet_id = tweet['id']
        created_at = pendulum.parse(tweet['created_at'], strict=False)
        t = csl(detail=json.dumps(tweet), created_at=created_at,
                user=user, api_url=resp.url, tweet_id=tweet_id)
        db.session.add(t)
        db.session.commit()


@app.route('/twitter/<int:user_id>/user_timeline')
def twitter_user_timeline(user_id):
    """
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    将用户 tweet 存入数据库
    """
    # FIXME: 用户授权验证
    screen_name = session.get('twitter_screen_name')
    if not screen_name:
        abort(401)

    user = db.session.query(models.User).get(user_id)

    # 获取数据库中最后 tweet
    last_tweet = get_user_last_tweet_or_mention(user, models.Tweet)

    # 获取 API 路径
    path = get_twitter_path(last_tweet, screen_name, 'tweet')

    # 访问 twitter API
    resp = twitter.get(path)
    assert resp.ok

    timeline = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    # 存入数据库
    save_twitter_data(resp, user, models.Tweet)

    # FIXME: response result
    return jsonify({'tweets': timeline})


@app.route('/twitter/<int:user_id>/mentions_timeline')
def twitter_mentions_timeline(user_id):
    """
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
    将用户 mentions 存入数据库
    """
    # FIXME: 用户授权验证
    screen_name = session.get('twitter_screen_name')
    if not screen_name:
        abort(401)

    user = db.session.query(models.User).get(user_id)

    # 获取数据库中最后 mention
    last_mention = get_user_last_tweet_or_mention(user, models.TweetMention)

    # 获取路径
    path = get_twitter_path(last_mention, screen_name, 'mention')

    # 更新最后 mention 之后的文章
    resp = twitter.get(path)
    assert resp.ok

    # 存入数据库
    save_twitter_data(resp, user, models.TweetMention)

    return jsonify(resp.json())


def count_filter_by_date(csl, user, start_date, end_date):
    """计算用户在时间范围内 cls 的数量

    args:
        user: 访问用户 User
        csl: 需要查找的表 例如，Tweet 或者 TweetMention
    retrun:
        用户在时间范围内 cls 的数量

    """
    print(csl.query.filter(
        csl.user == user,
        csl.created_at >= start_date,
        csl.created_at < end_date
    ))
    return csl.query.filter(
        csl.user == user,
        csl.created_at >= start_date,
        csl.created_at < end_date
    ).count()


@app.route('/twitter/<int:user_id>/summary')
def summary(user_id):
    user = models.User.query.get(user_id)

    start_date = pendulum.parse(request.args.get('start_date'), strict=False)
    end_date = pendulum.parse(request.args.get('end_date'), strict=False)

    tweet_count = count_filter_by_date(models.Tweet, user, start_date, end_date)
    mention_count = count_filter_by_date(models.TweetMention, user,
                                         start_date, end_date)

    result = {
        'tweets': tweet_count,
        'mentions': mention_count
    }
    return jsonify(result)


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
