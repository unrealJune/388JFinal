from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user
import uuid
from ..models import Playlist, User
from ..forms import SearchForm, PlaylistMetadataForm, PlaylistSongForm
from ..client import SongClient
playlists = Blueprint('playlists', __name__)

@playlists.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('playlists.search', query=form.search_query.data))
    
    #get top 10 playlists
    playlists = Playlist.objects.order_by('likes')[:10]

    #calculate duration of playlist
    for playlist in playlists:
        playlist.duration = 0
        for song in playlist.songs:
            track = SongClient().get_track_by_mbid(song)
            playlist.duration += track.get_duration()
            playlist.save()

    


    return render_template('index.html', title="Home", form=form, playlists=playlists)

#create playlist
@login_required
@playlists.route('/create', methods=['GET', 'POST'])
def create():
    #check if user is logged in
    if not current_user.is_authenticated:
        flash('You must be logged in to create a playlist', 'danger')
        return redirect(url_for('user.login'))
    else:
        form = PlaylistMetadataForm()
        if form.validate_on_submit():
            playlist = Playlist(name=form.name.data, description=form.description.data, owner=current_user._get_current_object(), uuid=str(uuid.uuid4()), songs=[])
            print(playlist.owner)
            playlist.save()
            return redirect(url_for('playlists.edit', uuid=playlist.uuid))

    return render_template('create.html', title="Create Playlist", form=form)

@playlists.route('/edit/<uuid>', methods=['GET', 'POST'])
def edit(uuid):
    playlist = Playlist.objects(uuid=uuid).first()
    if playlist is None or  playlist.owner != current_user._get_current_object():
        flash('You do not have permission to edit this playlist', 'danger')
        return redirect(url_for('playlists.index'))
    else:
        playForm = PlaylistSongForm()
        if playForm.validate_on_submit():
            song = SongClient().get_track(playForm.artist.data, playForm.song.data)
            
            try:
                mbid = song.get_mbid()
                print(song)
                playlist.songs.append(mbid)
                playlist.save()
                return redirect(url_for('playlists.edit', uuid=playlist.uuid))
            except:
                flash('Song not found', 'danger')
                return redirect(url_for('playlists.edit', uuid=playlist.uuid))

        form = PlaylistMetadataForm()
        if form.validate_on_submit():
            playlist.name = form.name.data
            playlist.description = form.description.data
            playlist.save()
            return redirect(url_for('playlists.edit', uuid=playlist.uuid))
        else:
            form.name.data = playlist.name
            form.description.data = playlist.description

        top15 = SongClient().get_top_tracks()
        songs = []

        for mbid in playlist.songs:
            songs.append(SongClient().get_track_by_mbid(mbid))



        return render_template('edit.html', title="Edit Playlist", form=form, playForm = playForm, songs=songs, playlist=playlist, top15=top15)

@playlists.route('/delete/<uuid>', methods=['GET', 'POST'])
def delete(uuid):
    playlist = Playlist.objects(uuid=uuid).first()
    if playlist is not None:
        if playlist.owner == current_user._get_current_object():
            playlist.delete()
            flash('Playlist deleted', 'success')
            return redirect(url_for('user.account'))
        else:
            flash('You do not have permission to delete this playlist', 'danger')
            return redirect(url_for('playlists.index'))
        
    else:
        flash('Playlist not found', 'danger')
        return redirect(url_for('user.account'))
    
@playlists.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('playlists.search', query=form.search_query.data))

    
    #get all playlists that match query
    playlists = Playlist.objects(name__icontains=query)


        #calculate duration of playlist
    for playlist in playlists:
        playlist.duration = 0
        for song in playlist.songs:
            track = SongClient().get_track_by_mbid(song)
            playlist.duration += track.get_duration()
            playlist.save()


    return render_template('search.html', title="Search", playlists=playlists, query=query, form=form)

@playlists.route('/deleteTrack/<mbid>/<uuid>', methods=['GET', 'POST'])
def deleteSong(uuid, mbid):
    playlist = Playlist.objects(uuid=uuid).first()
    if playlist is None or  playlist.owner != current_user._get_current_object():
        flash('You do not have permission to edit this playlist', 'danger')
        return redirect(url_for('playlists.index'))
    else:
        playlist.songs.remove(mbid)
        playlist.save()
        return redirect(url_for('playlists.edit', uuid=playlist.uuid))
    

@playlists.route('/addTrack/<mbid>/<uuid>', methods=['GET', 'POST'])
def addSong(uuid, mbid):
    playlist = Playlist.objects(uuid=uuid).first()
    if playlist is None or  playlist.owner != current_user._get_current_object():
        flash('You do not have permission to edit this playlist', 'danger')
        return redirect(url_for('playlists.index'))
    else:
        playlist.songs.append(mbid)
        playlist.save()
        return redirect(url_for('playlists.edit', uuid=playlist.uuid))
    
@playlists.route('/view/<uuid>', methods=['GET', 'POST'])
def view(uuid):
    playlist = Playlist.objects(uuid=uuid).first()
    if playlist is None:
        flash('Playlist not found', 'danger')
        return redirect(url_for('playlists.index'))
    else:
        songs = []

        for mbid in playlist.songs:
            songs.append(SongClient().get_track_by_mbid(mbid))
        
        form = SearchForm()
        if form.validate_on_submit():
            return redirect(url_for('playlists.search', query=form.search_query.data))
        
        total_duration = 0
        for song in songs:
            total_duration += song.get_duration()

        liked = False
        if current_user.is_authenticated:
            if playlist.uuid in current_user.liked_playlists:
                liked = True
            



        

        return render_template('view.html', title="View Playlist", playlist=playlist, songs=songs, form=form, total_duration=total_duration, liked=liked)
    

@playlists.route('/like/<uuid>', methods=['GET', 'POST'])
def like(uuid):
    if not current_user.is_authenticated:
        flash('You must be logged in to like a playlist', 'danger')
        return redirect(url_for('user.login'))
    else:
        playlist = Playlist.objects(uuid=uuid).first()
        if playlist is None:
            flash('Playlist not found', 'danger')
            return redirect(url_for('playlists.index'))
        else:
            if playlist.uuid in current_user.liked_playlists:
                current_user.liked_playlists.remove(playlist.uuid)
                current_user.save()
                playlist.likes = playlist.likes - 1
                playlist.save()
                return redirect(url_for('playlists.view', uuid=playlist.uuid))
            else:
                current_user.liked_playlists.append(playlist.uuid)
                current_user.save()
                playlist.likes += 1
                playlist.save()
                return redirect(url_for('playlists.view', uuid=playlist.uuid))