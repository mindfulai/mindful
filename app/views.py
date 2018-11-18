import json
import pendulum
import requests

from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.consumer import oauth_authorized, oauth_error

from flask_login import login_required, login_user, logout_user, current_user

from flask import request, session, redirect, url_for, \
    abort, render_template, flash, jsonify
from app import app, db
from app import models
from app import login_manager
from app.actions import get_user_last_tweet_or_mention, get_twitter_path,\
    save_twitter_data, get_twitter_screen_name, count_filter_by_date, \
    get_oauth_or_create

from app import actions


from sqlalchemy.orm.exc import NoResultFound

# Twitter
twitter_blueprint = make_twitter_blueprint(
    api_key="devnDViKMhTY4J5AwVKW7NewW",
    api_secret="92kwOgTnMiFNGP1bXNvaLCOLSEIiX6WYSPYDohEWIAnsDceGja",
)

# Facebook
facebook_blueprint = make_facebook_blueprint(
    client_id="176320989922581",
    client_secret="bfbf2231584f211669debf63467e58e9",
)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


##############################################
#             Facebook API
##############################################


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_auth(facebook_blueprint, token):
    """ Facebook 登录 """
    if not token:
        return False

    resp = facebook.get('me')

    if not resp.ok:
        return jsonify(resp.json())

    fb_name = resp.json()['name']
    fb_id = resp.json()['id']

    # Find this OAuth token in the database, or create it
    query = models.OAuth.query.filter_by(
        provider=facebook_blueprint.name,
        provider_user_id=fb_id,
    )

    try:
        # 查找用户授权
        oauth = query.one()
    except NoResultFound:
        # 创建 OAuth
        oauth = models.OAuth(
            provider=facebook_blueprint.name,
            provider_user_id=fb_id,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Facebook.")

    else:
        # Create a new local user account for this user
        user = models.User(username=fb_name)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(oauth.user)
        flash("Successfully signed in with Facebook.")

    # 更新 token
    actions.update_oauth_token(oauth, token)

    # 更新获取 posts
    print('=== get user posts')

    return redirect(url_for('facebook_posts'))


@app.route('/facebook/posts')
@login_required
def facebook_posts():
    """ 获取 Facebook posts """
    user = current_user

    # 保存 posts

    redirect_uri = 'https://pocoweb-mindful.herokuapp.com/facebook/posts'
    code = request.args.get('code')

    if not code:
        # 获取 code
        return redirect('https://www.facebook.com/dialog/oauth' +
                        '?client_id={}&redirect_uri={}&scope={}'.format(
                            facebook.client_id, redirect_uri, 'email,user_posts'
                        ))

    # 根据 code 换取 access_token
    url = 'https://graph.facebook.com/oauth/access_token'
    data = {
        'client_id': facebook.client_id,
        'redirect_uri': redirect_uri,
        'client_secret': facebook_blueprint.client_secret,
        'code': code
    }
    resp = requests.get(url, params=data)

    access_token = json.loads(resp.text)['access_token']

    # 使用 access_token 获取 posts
    resp = facebook.get('me?fields=posts&access_token={}'.format(access_token))

    if not resp.ok:
        return jsonify(resp.json())

    posts = resp.json()['posts']['data']

    for post in posts:
        created_at = pendulum.parse(post['created_time'])

        try:
            fb = db.session.query(models.FacebookPost).filter_by(
                post_id=post['id']).one()

        except NoResultFound:
            fb = models.FacebookPost(
                post_id=post['id'],
                created_at=created_at,
                detail=json.dumps(post),
                api_url=resp.url,
                user=user
            )
            db.session.add(fb)
            db.session.commit()

    return redirect('/static/dist/index.html#/index?name={}&id={}'.format(
        user.username, user.id))


@app.route('/facebook/<int:user_id>/summary')
@login_required
def facebook_summary(user_id):
    """ Facebook 数据统计 """
    user = models.User.query.get(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    period = request.args.get('period', 'day')

    start_date = dt.start_of(period)
    end_date = dt.end_of(period)

    posts = count_filter_by_date(
        models.FacebookPost, user, start_date, end_date)
    result = {
        'posts': posts,
    }
    return jsonify(result)


##############################################
#             Twitter API
##############################################

@oauth_authorized.connect_via(twitter_blueprint)
def twitter_auth(twitter_blueprint, token):
    """ Twitter 授权 """

    if not token:
        return False

    user = current_user

    resp = twitter.get("account/settings.json")
    if not resp.ok:
        if resp.json()['errors'][0]['message'] == "Invalid or expired token.":
            return redirect(url_for("twitter.login"))
        return jsonify(resp.json())

    screen_name = resp.json()['screen_name']
    oauth, created = get_oauth_or_create(twitter_blueprint, screen_name, user)

    actions.update_oauth_token(oauth, token)

    print('==== get twitter user timeline')
    twitter_user_timeline(user.id)
    print('==== get twitter user mention timeline')
    twitter_mentions_timeline(user.id)
    return redirect('/static/dist/index.html#/index?name={}&id={}'.format(
        user.username, user.id))


@app.route('/twitter/<int:user_id>/user_timeline')
@login_required
def twitter_user_timeline(user_id):
    """ 将用户 tweet 存入数据库
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    """
    user = db.session.query(models.User).get(user_id)

    screen_name = get_twitter_screen_name(twitter_blueprint, user)

    # 获取数据库中最后 tweet
    last_tweet = get_user_last_tweet_or_mention(user, models.Tweet)

    # 获取 API 路径
    path = get_twitter_path(last_tweet, screen_name, 'tweet')

    # 访问 twitter API
    resp = twitter.get(path)
    if not resp.ok:
        return jsonify(resp.json())

    timeline = json.dumps(resp.json(), indent=2, ensure_ascii=False)

    # 存入数据库
    save_twitter_data(resp, user, models.Tweet)

    # FIXME: response result
    return jsonify({'tweets': timeline})


@app.route('/twitter/<int:user_id>/mentions_timeline')
@login_required
def twitter_mentions_timeline(user_id):
    """ 将用户 mentions 存入数据库
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
    """
    user = db.session.query(models.User).get(user_id)

    screen_name = get_twitter_screen_name(twitter_blueprint, user)

    # 获取数据库中最后 mention
    last_mention = get_user_last_tweet_or_mention(user, models.TweetMention)

    # 获取路径
    path = get_twitter_path(last_mention, screen_name, 'mention')

    # 更新最后 mention 之后的文章
    resp = twitter.get(path)
    if not resp.ok:
        return jsonify(resp.json())

    # 存入数据库
    save_twitter_data(resp, user, models.TweetMention)

    return jsonify(resp.json())


@app.route('/twitter/<int:user_id>/summary')
@login_required
def twitter_summary(user_id):
    """ Twitter 统计数据 """
    user = models.User.query.get(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    period = request.args.get('period', 'day')

    start_date = dt.start_of(period)
    end_date = dt.end_of(period)

    tweet_count = count_filter_by_date(models.Tweet, user, start_date, end_date)
    mention_count = count_filter_by_date(models.TweetMention, user,
                                         start_date, end_date)

    result = {
        'tweets': tweet_count,
        'mentions': mention_count
    }
    return jsonify(result)


##############################################
#                 System
##############################################


@app.route('/logout')
@login_required
def logout():
    """User logout/authentication/session management."""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/user/<int:user_id>/authorized')
@login_required
def authorized(user_id):
    user = load_user(user_id)

    result = {
        'twitter_auth': actions.is_authorized(twitter_blueprint.name, user),
        'facebook_auth': actions.is_authorized(facebook_blueprint.name, user)
    }
    return jsonify(result)


##############################################
#                 Darksky
##############################################

darksky_secret = 'bec7b6450421ba2b12b42fec0d98ad72'


@app.route('/user/<int:user_id>/location', methods=['POST'])
def save_location(user_id):
    """ 保存用户地理位置 """
    user = load_user(user_id)
    user = models.User.query.get(user_id)
    data = request.json

    latitude = data['latitude']
    longitude = data['longitude']

    location = models.Location(
        user=user,
        latitude=latitude,
        longitude=longitude
    )

    db.session.add(location)
    db.session.commit()
    print({'msg': 'success'})
    return jsonify({'msg': 'success'})


@app.route('/debug')
def debug():
    tweets = db.session.query(models.Tweet).all()
    tweet_result = {'tweet': []}
    for tweet in tweets:
        tweet_result['tweet'].append({
            'id': tweet.id, 'user': tweet.user.username,
            'text': json.loads(tweet.detail)['text'],
            'api_url': tweet.api_url, 'tweet_id': tweet.tweet_id,
            'time': tweet.created_at})

    mentions = db.session.query(models.TweetMention).all()
    mention_result = {'mention': []}
    for mention in mentions:
        mention_result['mention'].append({
            'id': mention.id, 'user': mention.user.username,
            'text': json.loads(mention.detail)['text'],
            'api_url': mention.api_url})

    users = db.session.query(models.User).all()
    user_result = {'user': []}
    for u in users:
        user_result['user'].append({
            'name': u.username
        })

    oauths = db.session.query(models.OAuth).all()
    oauth_result = {'oauth': []}
    for oauth in oauths:
        oauth_result['oauth'].append({
            'provider': oauth.provider,
            'username': oauth.user.username,
            'provider_user_id': oauth.provider_user_id
        })

    fbs = db.session.query(models.FacebookPost).all()
    fb_result = {'fb': []}
    for fb in fbs:
        fb_result['fb'].append({
            'id': fb.id, 'user': fb.user.username,
            'text': json.loads(fb.detail),
            'api_url': fb.api_url})

    return jsonify(user_result, '=======',
                   oauth_result, '=======',
                   tweet_result, '=======',
                   mention_result, '=======',
                   fb_result, '=======')


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
