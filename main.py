import os

from flask import Flask, request, redirect, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64) #key for flask session

client_id = '421d10fb54904c7090f7b20f76be3980' #store these securely
client_secret = 'f4e9f9165d4d4fa5853f09fd2c313401'
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private' #comma sepeate to add more scopes

cache_handler = FlaskSessionCacheHandler(session)

#auth code flow mechanism for auth
sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    cache_handler = cache_handler,
    show_dialog = True # debug
)

#client to interact with spotify api
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    playlist_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlist_html = '<br>'.join([f'{name}: {url}' for name, url in playlist_info])
    return playlist_html

@app.route('/get_random_playlist_tracks')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)