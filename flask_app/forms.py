from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        #check if there is a capital letter
        if not any(char.isupper() for char in password.data):
            raise ValidationError("Password must contain at least one capital letter")
        #check if includes number and special character
        specialchars= '!@#$%^&*()_+{}|:"<>?`-=[]\;\',./'
        if not any(char.isdigit() for char in password.data) and not any(char in specialchars for char in password.data):
            raise ValidationError("Password must contain at least one number and special character" )
        
        


    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")
        
class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

class PlaylistMetadataForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=1, max=50)])
    description = TextAreaField("Description", validators=[Length(min=5, max=1000), InputRequired()])
    submit = SubmitField("Submit")

class PlaylistSongForm(FlaskForm):
    song = StringField("Song", validators=[InputRequired(), Length(min=1, max=100)])
    artist = StringField("Artist", validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField("Submit")
    