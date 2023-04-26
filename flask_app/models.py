from flask_login import UserMixin
from datetime import datetime
from . import db
from . import config
import base64


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    liked_playlists = db.ListField(db.StringField(), default=[])

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Playlist(db.Document):
    #list of songs
    songs = db.ListField(db.StringField(), default=[])
    #name of playlist
    name = db.StringField(required=True)
    #owner of playlist
    owner = db.ReferenceField(User, required=True)
    #date created
    date_created = db.DateTimeField(default=datetime.utcnow)
    #date last modified
    date_modified = db.DateTimeField(default=datetime.utcnow)
    #description of playlist
    description = db.StringField(required=True)
    #likes
    likes = db.IntField(default=0)
    #uuid
    uuid = db.StringField(required=True, unique=True)


    
