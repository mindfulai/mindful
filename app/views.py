import json
import pendulum
import requests
import decimal
import os

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
    get_oauth_or_create, get_user_oauth, is_token_expired, \
    get_all_objects_filter_by_date

from app import actions
from app.azure import sentiment, azure

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend

from fitbit import Fitbit

# Twitter
twitter_blueprint = make_twitter_blueprint(
    api_key=os.getenv('TWITTER_APP_ID'),
    api_secret=os.getenv('TWITTER_SECRET'),
)

# Facebook
facebook_blueprint = make_facebook_blueprint(
    client_id=os.getenv('FACEBOOK_APP_ID'),
    client_secret=os.getenv('FACEBOOK_SECRET'),
    scope="email,user_posts"
)


twitter_blueprint.backend = SQLAlchemyBackend(models.OAuth,
                                              db.session, user=current_user)
facebook_blueprint.backend = SQLAlchemyBackend(models.OAuth,
                                               db.session, user=current_user)


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
        # flash("Successfully signed in with Facebook.")

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
        # flash("Successfully signed in with Facebook.")

    # 更新 token
    actions.update_oauth_token(oauth, token)

    # 更新获取 posts
    print('=== get user posts')
    facebook_posts(oauth.user.id)

    return redirect('/#/index?name={}&id={}'.format(
        oauth.user.username, oauth.user.id))


@app.route('/user/<int:user_id>/facebook/posts/update')
@login_required
def facebook_posts(user_id):
    """ 获取 Facebook posts

    API: https://developers.facebook.com/docs/graph-api/reference/v3.2/user/feed
    """
    user = load_user(user_id)

    if not facebook.authorized:
        return redirect(url_for('facebook.login'))

    last_post = models.FacebookPost.query.filter_by(
        user=user).order_by(models.FacebookPost.created_at.desc()).first()

    if last_post:
        last_post_time = pendulum.instance(last_post.created_at).timestamp()
        resp = facebook.get('v3.2/me/feed?since={}'.format(last_post_time))
    else:
        resp = facebook.get('v3.2/me/feed')

    if not resp.ok:
        app.logger.error(resp.json())
        return jsonify(resp.json())

    posts = resp.json()['data']

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
            if json.loads(fb.detail).get('message'):
                result = azure(fb.id, json.loads(fb.detail)['message'])
                for row in result['documents']:
                    print('======== create sentiment ')
                    sentiment = models.Sentiment(
                        score=row['score'], language='en')
                    db.session.add(sentiment)
                    db.session.commit()
                fb.sentiment = sentiment
                fb.sentiment_id = sentiment.id
                db.session.add(fb)
                db.session.commit()

    return jsonify({"msg": "success"})


@app.route('/user/<int:user_id>/facebook/summary')
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


@app.route('/user/<int:user_id>/facebook/sentiment')
def facebook_sentiment_list(user_id):
    user = load_user(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    start_date = dt.start_of('day')
    end_date = dt.end_of('day')

    posts = get_all_objects_filter_by_date(
        models.FacebookPost, user, start_date, end_date)

    result = []

    for post in posts:
        print(post.detail)
        if json.loads(post.detail).get('message'):
            row = {
                'created_at': post.created_at,
                'content': json.loads(post.detail)['message'],
                'score': post.sentiment.score
            }
            result.append(row)
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
    oauth, created = get_oauth_or_create(
        twitter_blueprint.name, user, screen_name)

    actions.update_oauth_token(oauth, twitter.token)

    print('==== get twitter user timeline')
    twitter_user_timeline(user.id)
    print('==== get twitter user mention timeline')
    twitter_mentions_timeline(user.id)
    return redirect('/#/index?name={}&id={}'.format(
        user.username, user.id))


@app.route('/user/<int:user_id>/twitter/user_timeline/update')
@login_required
def twitter_user_timeline(user_id):
    """ 将用户 tweet 存入数据库
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    """

    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

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

    return jsonify({'msg': 'success'})


@app.route('/user/<int:user_id>/twitter/mentions_timeline/update')
@login_required
def twitter_mentions_timeline(user_id):
    """ 将用户 mentions 存入数据库
    API: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
    """

    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

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

    return jsonify({'msg': 'success'})


@app.route('/user/<int:user_id>/twitter/summary')
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


@app.route('/user/<int:user_id>/twitter/sentiment')
def twitter_sentiment_list(user_id):
    user = load_user(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    start_date = dt.start_of('day')
    end_date = dt.end_of('day')

    tweets = get_all_objects_filter_by_date(
        models.Tweet, user, start_date, end_date)

    result = []

    for tweet in tweets:
        row = {
            'created_at': tweet.created_at,
            'content': json.loads(tweet.detail)['text'],
            'score': tweet.sentiment.score
        }
        result.append(row)
    return jsonify(result)


##############################################
#                 System
##############################################


@app.route('/logout')
@login_required
def logout():
    """User logout/authentication/session management."""
    # flash('You were logged out')
    print(session['facebook_auth_token'])
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/user/<int:user_id>/authorized')
@login_required
def authorized(user_id):
    user = load_user(user_id)

    result = {
        'twitter_auth': actions.is_authorized(twitter_blueprint.name, user),
        'facebook_auth': actions.is_authorized(facebook_blueprint.name, user),
        'fitbit_auth': actions.is_authorized('fitbit', user)
    }
    return jsonify(result)


##############################################
#                 Darksky
##############################################


@app.route('/user/<int:user_id>/location_and_weather/create', methods=['POST'])
def location_and_weather_create(user_id):
    """ 保存用户所在的地理位置与天气 """
    user = load_user(user_id)
    data = request.json

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if not latitude or not longitude:
        return jsonify({'msg': 'Error latitude or longitude'})

    # 保存地理位置
    actions.save_location(user, latitude, longitude)
    # 保存天气
    result = actions.save_and_get_weather(user, latitude, longitude)
    return jsonify(result)


##############################################
#                 Mood
##############################################

@app.route('/user/<int:user_id>/mood/create', methods=['POST'])
def mood_create(user_id):
    """ 创建用户心情
    """
    user = load_user(user_id)
    data = request.json

    detail = data['detail']
    score = data['score']

    mood = models.Mood(user=user, detail=detail, score=score)
    db.session.add(mood)
    db.session.commit()

    result = azure(mood.id, mood.detail)
    print(result)
    for row in result['documents']:
        print('======== create sentiment ')
        sentiment = models.Sentiment(score=row['score'], language='en')
        db.session.add(sentiment)
        db.session.commit()

    mood.sentiment = sentiment
    mood.sentiment_id = sentiment.id
    db.session.add(mood)
    db.session.commit()

    return jsonify({'msg': 'success'})


@app.route('/user/<int:user_id>/mood/list')
def mood_list(user_id):
    user = load_user(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    start_date = dt.start_of('day')
    end_date = dt.end_of('day')

    moods = models.Mood.query.filter(
        models.Mood.user == user,
        models.Mood.created_at >= start_date,
        models.Mood.created_at <= end_date
    ).order_by(models.Mood.created_at.desc()).all()

    result = []
    for mood in moods:
        result.append({
            'datetime': mood.created_at,
            'score': mood.score,
            'detail': mood.detail
        })
    print(result)

    return jsonify(result)


@app.route('/user/<int:user_id>/mood/average/list')
def mood_average_list(user_id):
    """ 展示用户每日心情平均值列表 """
    user = load_user(user_id)

    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    period = request.args.get('period')
    start_date = dt.start_of(period)
    end_date = dt.end_of(period)

    moods = db.session.query(func.avg(models.Mood.score).label('average'), func.date(
        models.Mood.created_at).label('date')).filter(
            models.Mood.user == user,
            models.Mood.created_at >= start_date,
            models.Mood.created_at <= end_date
    ).group_by('date').all()

    result = []
    for mood in moods:
        info = {
            'date': mood.date,
            'score': int(decimal.Decimal(mood.average).quantize(
                decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP)),
        }

        dt = pendulum.parse(str(mood.date))
        if period == 'week':
            info['day'] = dt.day_of_week
        elif period == 'month':
            info['day'] = dt.day
        elif period == 'year':
            info['day'] = dt.day_of_year

        result.append(info)

    return jsonify(result)


@app.route('/user/<int:user_id>/mood/sentiment')
def mood_sentiment_list(user_id):
    user = load_user(user_id)
    dt = pendulum.parse(request.args.get('datetime'), strict=False)
    start_date = dt.start_of('day')
    end_date = dt.end_of('day')

    moods = get_all_objects_filter_by_date(
        models.Mood, user, start_date, end_date)

    result = []

    for mood in moods:
        print(mood.detail)
        row = {
            'created_at': mood.created_at,
            'content': mood.detail,
            'score': mood.sentiment.score
        }
        result.append(row)
    return jsonify(result)


##############################################
#                 Fitbit
##############################################


@app.route('/login/fitbit')
@login_required
def fitbit_auth():
    user = current_user
    fitbit = Fitbit(client_id=os.getenv('FITBIT_APP_ID'),
                    client_secret=os.getenv('FITBIT_SECRET'),
                    redirect_uri=url_for('fitbit_auth', _external=True))

    code = request.args.get('code')
    if not code:
        url, _ = fitbit.client.authorize_token_url()
        return redirect(url)

    token = fitbit.client.fetch_access_token(code=code)

    oauth, created = get_oauth_or_create('fitbit', user, token['user_id'])
    app.logger.info('======== \n{} access_token: {}'.format(
        user.username, oauth.token))
    actions.update_oauth_token(oauth, token)

    return redirect('/#/index?name={}&id={}'.format(user.username, user.id))


@app.route('/user/<int:user_id>/fitbit/sleep/day')
@login_required
def fitbit_sleep(user_id):
    """ 创建或更新今天的 sleep 记录
    API: https://dev.fitbit.com/build/reference/web-api/sleep/
    """
    user = load_user(user_id)
    oauth = get_user_oauth(user=user, provider='fitbit')

    if not oauth:
        return jsonify({'msg': 'Unauthorized'})

    fitbit = Fitbit(client_id=os.getenv('FITBIT_APP_ID'),
                    client_secret=os.getenv('FITBIT_SECRET'),
                    access_token=oauth.token['access_token'],
                    refresh_token=oauth.token['refresh_token'])

    # TODO: 如果没有 datetime 参数处理
    dt_str = request.args.get('datetime')
    dt = pendulum.parse(dt_str, strict=False)

    sleep_data = fitbit.sleep(date=dt.date(), user_id=oauth.provider_user_id)

    query = models.Sleep.query.filter_by(
        user=user,
        date=dt.date()
    )

    try:
        sleep = query.one()
        sleep.data = sleep_data
        db.session.add(sleep)
        db.session.commit()
    except NoResultFound:
        sleep = models.Sleep(
            user=user,
            data=sleep_data,
            date=dt.date()
        )
        db.session.add(sleep)
        db.session.commit()

    return jsonify(sleep.data['summary'])


@app.route('/user/<int:user_id>/fitbit/sleep/week')
@login_required
def fitbit_sleep_week(user_id):
    """ 每周的睡眠数据 """
    user = load_user(user_id)
    dt_str = request.args.get('datetime')
    dt = pendulum.parse(dt_str, strict=False)
    start_date = dt.start_of('week')
    end_date = dt.end_of('week')

    sleep = models.Sleep.query.filter(
        models.Sleep.user == user,
        models.Sleep.date >= start_date,
        models.Sleep.date <= end_date
    ).all()

    result = []
    for row in sleep:
        data = row.data['summary']
        data['day'] = pendulum.parse(str(row.date)).day_of_week
        result.append(data)

    return jsonify(result)


@app.route('/user/<int:user_id>/fitbit/activity/day')
@login_required
def fitbit_activity(user_id):
    """ 存储今天的 activity 记录
    API: https://dev.fitbit.com/build/reference/web-api/activity/
    """
    user = load_user(user_id)
    oauth = get_user_oauth(user=user, provider='fitbit')

    if not oauth:
        return jsonify({'msg': 'Unauthorized'})

    fitbit = Fitbit(client_id=os.getenv('FITBIT_APP_ID'),
                    client_secret=os.getenv('FITBIT_SECRET'),
                    access_token=oauth.token['access_token'],
                    refresh_token=oauth.token['refresh_token'],
                    refresh_cb=actions.fitbit_refresh_cb)

    dt_str = request.args.get('datetime')
    dt = pendulum.parse(dt_str, strict=False)

    # 如果 token 失效更新 token
    if is_token_expired(dt, oauth.token):
        new_token = fitbit.client.refresh_token()
        app.logger.info('=== {} new_token: {}'.format(user.username, new_token))
        actions.update_oauth_token(oauth, new_token)

    # 获取 activity
    data = fitbit.activities(date=dt.date(), user_id=oauth.provider_user_id)
    print('==== activities from fitbit')
    print(data)

    query = models.Activity.query.filter_by(
        user=user,
        date=dt.date()
    )

    try:
        activities = query.one()
        activities.data = data
        db.session.add(activities)
        db.session.commit()
    except NoResultFound:
        # 存储 activity
        activities = models.Activity(
            user=user,
            data=data,
            date=dt.date()
        )
        db.session.add(activities)
        db.session.commit()

    result = activities.data['summary']

    for distance in result['distances']:
        if distance['activity'] == 'total':
            result['distances'] = distance['distance']
            break

    return jsonify(result)


@app.route('/user/<int:user_id>/fitbit/activity/week')
@login_required
def fitbit_activity_week(user_id):
    """ 每周的 activities 数据 """
    user = load_user(user_id)
    dt_str = request.args.get('datetime')
    dt = pendulum.parse(dt_str, strict=False)
    start_date = dt.start_of('week')
    end_date = dt.end_of('week')

    activities = models.Activity.query.filter(
        models.Activity.user == user,
        models.Activity.date >= start_date,
        models.Activity.date <= end_date
    ).all()

    result = []
    for row in activities:
        data = row.data['summary']
        for distance in data['distances']:
            if distance['activity'] == 'total':
                data['distances'] = distance['distance']
                break
        data['day'] = pendulum.parse(str(row.date)).day_of_week

        result.append(data)

    return jsonify(result)


@app.route('/debug')
def debug():
    tweets = db.session.query(models.Tweet).all()
    tweet_result = {'tweet': []}
    for tweet in tweets:
        tweet_result['tweet'].append({
            'id': tweet.id, 'user': tweet.user.username,
            'text': json.loads(tweet.detail)['text'],
            'api_url': tweet.api_url, 'tweet_id': tweet.tweet_id,
            'time': tweet.created_at,
            'score': tweet.sentiment.score if tweet.sentiment else None})

    mentions = db.session.query(models.TweetMention).all()
    mention_result = {'mention': []}
    for mention in mentions:
        mention_result['mention'].append({
            'id': mention.id, 'user': mention.user.username,
            'text': json.loads(mention.detail)['text'],
            'api_url': mention.api_url,
            'score': mention.sentiment.score if mention.sentiment else None})

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
            'api_url': fb.api_url,
            'score': fb.sentiment.score if fb.sentiment else None
        })

    moods = db.session.query(models.Mood).all()
    mood_result = {'mood': []}
    for mood in moods:
        mood_result['mood'].append({
            'id': mood.id, 'user': mood.user.username,
            'text': mood.detail,
            'score': mood.sentiment.score if mood.sentiment else None
        })

    return jsonify(user_result, '=======',
                   oauth_result, '=======',
                   tweet_result, '=======',
                   mention_result, '=======',
                   fb_result, '=======',
                   mood_result, '=======')


@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    # flash('New entry was successfully posted')
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
        # flash('The entry was deleted.')
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
