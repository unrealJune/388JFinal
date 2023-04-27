import os
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Track:
    #constructor
    def __init__(self, name, artist, album, mbid, image, preview_url, duration):
        self.name = name
        self.artist = artist
        self.album = album
        self.mbid = mbid
        self.image = image
        self.preview_url = preview_url
        self.duration = duration



class SongClient():
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    def get_track(self, artist, query):
        #get track id
        res = self.sp.search(q='artist:' + artist + ' track:' + query, type='track')
        #throw error if no results
        if len(res['tracks']['items']) == 0:
            return None
        id = res['tracks']['items'][0]['id']
        
    
        return self.get_track_by_mbid(id)
    
    def get_track_by_mbid(self, mbid):
        res = self.sp.track(mbid)
        track = Track(res['name'], res['artists'][0]['name'], res['album']['name'], mbid ,  res['album']['images'][0]['url'], res['preview_url'], res['duration_ms'])
       
        return track
 
    
    def get_topN_tracks(self, n, artist):
        res = self.sp.search(q='artist:' + str(artist), type='track', limit=int(n))
        tracks = []
        for track in res['tracks']['items']:
            tracks.append(Track(track['name'], track['artists'][0]['name'], track['album']['name'], track['id'], track['album']['images'][0]['url'], track['preview_url'], track['duration_ms']))
        return tracks
    




    
    

