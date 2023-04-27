from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_talisman import Talisman


# stdlib
from datetime import datetime
import os


csp = {
    "default-src": [
        '\'self\'',
    ],
    'script-src': [
        'https://code.getmdl.io',
        '\'unsafe-inline\''
        
    ],

    'style-src': [
        'https://code.getmdl.io',
        'https://fonts.googleapis.com',
        'https://fonts.gstatic.com',
        '\'unsafe-inline\'',
    ],
    'font-src': [
        'https://fonts.googleapis.com',
        'https://fonts.gstatic.com',
    ],
    'img-src': [
        '\'self\'',
        'https://lastfm.freetls.fastly.net',
        'https://lastfm-img2.akamaized.net',
    ],
    
}
        



db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
from .playlists.routes import playlists
from .user.routes import user

from .models import User

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)

    if(test_config is not None):
        app.config.update(test_config)

    Talisman(app, content_security_policy=csp)  
    # Initialize database
    db.init_app(app)
    

    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_error_handler(404, page_not_found)

    
    app.register_blueprint(playlists)
    app.register_blueprint(user)


    login_manager.login_view = "user.login"
    

    return app

