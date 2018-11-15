import os
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
SQLALCHEMY_DATABASE_URI = 'postgres://qmxhgnyiiodlvx:daa9a651a943da6dc677f120e09d281bda1a48d4b7d77633e5b44b3b548663c6@ec2-75-101-138-165.compute-1.amazonaws.com:5432/dbe6bab21fo60n'
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-super-secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Twitter App
    TWITTER_API_KEY = os.environ.get(
        'TWITTER_API_KEY') or 'devnDViKMhTY4J5AwVKW7NewW'
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET') or\
        '92kwOgTnMiFNGP1bXNvaLCOLSEIiX6WYSPYDohEWIAnsDceGja'
