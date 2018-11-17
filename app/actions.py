import json
import pendulum

from sqlalchemy.orm.exc import NoResultFound
from flask import abort, flash

from app import db, models


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
        tweet_id = tweet['id_str']
        created_at = pendulum.parse(tweet['created_at'], strict=False)
        try:
            t = csl.query.filter_by(tweet_id=tweet_id).one()

        except NoResultFound:
            t = csl(detail=json.dumps(tweet), created_at=created_at,
                    user=user, api_url=resp.url, tweet_id=tweet_id)
            db.session.add(t)
            db.session.commit()


def get_twitter_screen_name(buleprint, user):
    query = models.OAuth.query.filter_by(
        provider=buleprint.name,
        user=user
    )

    try:
        oauth = query.one()
    except NoResultFound:
        # FIXME: twitter oauth required
        flash('Authoriza twitter firsh')
        abort(401)

    screen_name = oauth.provider_user_id
    return screen_name


def count_filter_by_date(csl, user, start_date, end_date):
    """计算用户在时间范围内 cls 的数量

    args:
        user: 访问用户 User
        csl: 需要查找的表 例如，Tweet 或者 TweetMention
    retrun:
        用户在时间范围内 cls 的数量

    """
    return csl.query.filter(
        csl.user == user,
        csl.created_at >= start_date,
        csl.created_at < end_date
    ).count()


def get_oauth_or_create(user_id, user):
    """获取或创建oauth
    args:
        user_id: 第三方授权的 user_id
        user: 访问用户 object
    return:
        oauth: OAuth
        created: 是否创建
    """
    query = models.OAuth.query.filter_by(
        provider=twitter_blueprint.name,
        provider_user_id=user_id
    )

    try:
        oauth = query.one()
        created = False
    except NoResultFound:
        oauth = models.OAuth(
            provider=twitter_blueprint.name,
            provider_user_id=user_id,
            user=user
        )
        db.session.add(oauth)
        db.session.commit()
        created = True
    return oauth, created
