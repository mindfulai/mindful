from app import db

from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_utils import JSONType


class Flaskr(db.Model):

    __tablename__ = "flaskr"

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<title {}>'.format(self.body)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    api_url = db.Column(db.String)
    detail = db.Column(db.String)


class TweetMention(db.Model):
    __tablename__ = "tweet_mentions"

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    api_url = db.Column(db.String)
    detail = db.Column(db.String)


class FacebookPost(db.Model):
    __tablename__ = "faceboot_posts"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    api_url = db.Column(db.String)
    detail = db.Column(db.String)


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())


class Weather(db.Model):
    __tablename__ = "weathers"

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_at = db.Column(db.DateTime, server_default=func.now())
    data = db.Column(MutableDict.as_mutable(JSONType))
    api_url = db.Column(db.String)


class Mood(db.Model):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_at = db.Column(db.DateTime, server_default=func.now())
    detail = db.Column(db.String)
    score = db.Column(db.Integer)


class Sleep(db.Model):
    __tablename__ = 'sleep'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    date = db.Column(db.Date)
    data = db.Column(MutableDict.as_mutable(JSONType))
    api_url = db.Column(db.String)
