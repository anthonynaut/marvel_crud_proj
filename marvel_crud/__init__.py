from flask import Flask
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


from .models import db as root_db, login_manager, ma

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

from flask_cors import CORS

from marvel_crud.helpers import JSONEncoder

app = Flask(__name__)



app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app,root_db)

login_manager.init_app(app)
login_manager.login_view = 'signin' # Specify what page to load for NON-AUTHED users

ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)

from marvel_crud import models