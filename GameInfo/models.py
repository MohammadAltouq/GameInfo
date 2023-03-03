from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    username = db.Column(db.String(),nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_crreated = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    profile_img = db.Column(db.String(), nullable = True)
    fav = db.relationship('Fav_games', backref = 'owner', lazy = True)

    def __init__(self,first_name, last_name, email, username, password, id = '', token = '',profile_img = '../static/images/profile.jpg'):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.profile_img = profile_img
        self.token = self.set_token(24)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    def __repr__(self):
        return f"User {self.email} has been added to the database!"

class Fav_games(db.Model):
    id = db.Column(db.String, primary_key = True)
    user_token=db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    #search
    rawg_id= db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    released = db.Column(db.String, nullable = True)
    genres = db.Column(db.String, nullable = True)
    tags = db.Column(db.String, nullable = True)
    img = db.Column(db.String, nullable = False)
    #details
    website = db.Column(db.String, nullable = True)
    platforms = db.Column(db.String, nullable = True)

    def __init__(self, user_token, rawg_id, name, released, genres, tags, img, website, platforms, id=''):
        self.id = self.set_id()
        self.user_token = user_token
        self.rawg_id = rawg_id
        self.name = name
        self.released = released
        self.genres = genres
        self.tags = tags
        self.img = img
        self.website = website
        self.platforms = platforms

    def set_id(self):
        return secrets.token_urlsafe()
    
    def __repr__(self):
        return f"{self.name} has been added to your list"
