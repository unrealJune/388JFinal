from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..models import User, Playlist
from ..forms import LoginForm, RegistrationForm, SearchForm
from ..client import SongClient

user = Blueprint("user", __name__)

@user.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("playlists.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You have been logged in!", "success")
            return redirect(url_for("playlists.index"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")


    return render_template("login.html", form=form)

    

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("playlists.index"))

@user.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("playlists.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("user.login"))
    
    print(form.errors)

    return render_template("register.html", title="Register", form=form)

@login_required
@user.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        flash('You must be logged in to view your account', 'danger')
        return redirect(url_for('user.login'))
    else:
    
        playlists = Playlist.objects(owner=current_user._get_current_object())
        #calculate duration of each playlist
        for playlist in playlists:
            playlist.duration = 0
            for mbid in playlist.songs:
                song = SongClient().get_track_by_mbid(mbid)
                playlist.duration += song.duration
            playlist.save()
        
        form = SearchForm()
        if form.validate_on_submit():
            return redirect(url_for('playlists.search', query=form.search_query.data))
        
        #calculate total duration of all playlists
        total_duration = 0
        total_likes  = 0
        for playlist in playlists:
            total_duration += playlist.duration
            total_likes += playlist.likes

        
        return render_template('account.html', title="Account", form=form ,playlists=playlists, total_duration=total_duration, total_likes=total_likes, user = current_user._get_current_object())

#view other users' accounts
@user.route('/view_account/<username>', methods=['GET', 'POST'])
def view_account(username):
    #get playlists of user
    user = User.objects(username=username).first()
    print(user)
    playlists = Playlist.objects(owner=user)
    #calculate duration of each playlist

    for playlist in playlists:
        playlist.duration = 0
        for mbid in playlist.songs:
            song = SongClient().get_track_by_mbid(mbid)
            playlist.duration += song.duration
        playlist.save()

    #calculate total duration of all playlists
    total_duration = 0
    total_likes  = 0
    for playlist in playlists:
        total_duration += playlist.duration
        total_likes += playlist.likes

    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('playlists.search', query=form.search_query.data))
    
    return render_template('view_account.html', title="Account", playlists=playlists, total_duration=total_duration, total_likes=total_likes, user = user, form = form)