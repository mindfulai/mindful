from app import db


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

class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime)
    user = db.Column(db.String)
    api_url = db.Column(db.String)
    content = db.Column(db.String)
