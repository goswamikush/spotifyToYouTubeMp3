import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
from getVideoIds import get_video_ids
from downloadSongs import download_songs

#Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

scope = 'user-library-read playlist-modify-public playlist-modify-private'

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdnjkassdasj$#*sasfa%@'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth(scope).get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth(scope).get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    return redirect(url_for('saved_liked_songs', external=True))

@app.route('/savedLikedSongs')
def saved_liked_songs():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    current_songs_json = sp.current_user_saved_tracks(limit=20)
    current_songs = []

    for item in current_songs_json['items']:
        current_songs.append(item['track']['name'])

    videoIds = get_video_ids(current_songs)
    download_songs(videoIds)

    return current_songs

def get_token():
    token_info = session.get(TOKEN_INFO, None)

    if not token_info:
        redirect(url_for('login', external=False))

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        spotify_oauth = create_spotify_oauth(scope)
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth(scope):
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('redirect_page', _external=True),
        scope=scope
        )

app.run(debug=True)
