from app import db

from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin


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


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    api_url = db.Column(db.String)
    detail = db.Column(db.String)


class TweetMention(db.Model):
    __tablename__ = "tweet_mentions"

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    api_url = db.Column(db.String)
    detail = db.Column(db.String)
