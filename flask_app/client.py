import pylast
import os
import pprint

#get API ket from OS
API_KEY = os.environ.get('LASTFM_KEY')
API_SECRET = os.environ.get('LASTFM_SECRET')

class SongClient():
    def __init__(self):
        self.network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    
    def search_song(self, artist, query):
        res = self.network.search_for_track(track_name=query, artist_name=artist)
        return res.get_next_page()
    
    def get_track(self, artist, query):
        res = self.network.get_track(artist, query)
        return res
    
    def get_track_by_mbid(self, mbid):
        res = self.network.get_track_by_mbid(mbid)
        return res
    
    def get_topN_tracks(self, n):
        out = []
        res = self.network.get_geo_top_tracks(country="United States", location=None, limit=n * 2, cacheable=True) 
        for track in res:
          
            if len(out) < n and track.item.get_mbid() is not None:
                out.append(track.item)
            
            #print album art
            #print(track.item.get_cover_image())
            
    
        return out
    

        


