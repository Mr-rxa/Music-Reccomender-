import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# ---- Spotify API Setup ----
SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# ---- YouTube API Setup ----
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

# ---- CSS Styling (your existing CSS here) ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(315deg, 
            #4f2991 3%, 
            #7dc4ff 38%, 
            #36cfcc 68%, 
            #a92ed3 98%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif !important;
        color: #FFFFFF;
        min-height: 100vh;
        padding: 2rem;
    }

    .song-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }

    .song-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    a {
        color: #FFD700;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.25rem;
    }

    a:hover {
        text-decoration: underline;
    }

    select, button {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Mood Selection ----
moods = ["happy", "sad", "energetic", "relaxed", "romantic"]
st.title("🎵 Mood-Based Music Recommendation")
st.write("Select your current mood and get personalized music recommendations from Spotify & YouTube.")

mood = st.selectbox("Choose your mood:", options=moods, index=0)

# ---- Fetch Songs from Spotify ----
def get_spotify_tracks(mood, limit=10):
    try:
        results = sp.search(q=mood, type='track', limit=limit)
        tracks = []
        for item in results['tracks']['items']:
            title = item['name'] + " - " + item['artists'][0]['name']
            url = item['external_urls']['spotify']
            tracks.append(("Spotify", title, url))
        return tracks
    except Exception as e:
        st.error(f"Spotify API error: {e}")
        return []

# ---- Fetch Songs from YouTube ----
def get_youtube_tracks(mood, limit=10):
    try:
        params = {
            'part': 'snippet',
            'q': f"{mood} song",
            'type': 'video',
            'key': YOUTUBE_API_KEY,
            'maxResults': limit,
        }
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        videos = response.json().get('items', [])
        tracks = []
        for video in videos:
            title = video['snippet']['title']
            video_id = video['id']['videoId']
            url = f"https://www.youtube.com/watch?v={video_id}"
            tracks.append(("YouTube", title, url))
        return tracks
    except Exception as e:
        st.error(f"YouTube API error: {e}")
        return []

# ---- Function to get one random song from combined lists ----
def get_random_song(mood):
    spotify_tracks = get_spotify_tracks(mood)
    youtube_tracks = get_youtube_tracks(mood)
    combined = spotify_tracks + youtube_tracks
    if not combined:
        return None
    return random.choice(combined)

# ---- Session state to store current song ----
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# ---- Refresh button ----
if st.button("🔄 Refresh Song"):
    st.session_state.current_song = get_random_song(mood)

# ---- If no song selected yet, fetch one ----
if st.session_state.current_song is None:
    st.session_state.current_song = get_random_song(mood)

# ---- Display the current song ----
if st.session_state.current_song:
    platform, title, url = st.session_state.current_song
    st.markdown(
        f"""
        <div class="song-card">
            <p><strong>{platform} Recommendation:</strong></p>
            <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.warning("No songs found for this mood. Try refreshing or selecting a different mood.")
