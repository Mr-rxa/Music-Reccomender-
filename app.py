import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# ---- Spotify API Setup ----
SPOTIFY_CLIENT_ID = 'db5ac0f57dad40d684b53c5bb66e16fd'
SPOTIFY_CLIENT_SECRET = 'eb9666c0bed6444db4c1b0bca524a7a3'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# ---- CSS Styling ----
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
st.write("Select your current mood and get personalized music recommendations from Spotify.")

mood = st.selectbox("Choose your mood:", options=moods, index=0)

# ---- Fetch a large pool of Spotify tracks for each mood ----
def fetch_spotify_tracks(mood, total=400):
    tracks = []
    seen_ids = set()
    max_limit = 50  # Spotify API max per request
    for offset in range(0, total, max_limit):
        try:
            results = sp.search(q=mood, type='track', limit=max_limit, offset=offset)
            items = results['tracks']['items']
            if not items:
                break
            for item in items:
                track_id = item['id']
                if track_id not in seen_ids:
                    seen_ids.add(track_id)
                    title = item['name'] + " - " + item['artists'][0]['name']
                    url = item['external_urls']['spotify']
                    tracks.append((title, url))
            if len(items) < max_limit:
                break  # No more results
        except Exception as e:
            st.error(f"Spotify API error: {e}")
            break
    random.shuffle(tracks)
    return tracks

# ---- Session State Management ----
if "track_pools" not in st.session_state:
    st.session_state.track_pools = {}  # mood -> full track list

if "track_indices" not in st.session_state:
    st.session_state.track_indices = {}  # mood -> index of next song to show

# ---- Load tracks for the selected mood if not already loaded ----
if mood not in st.session_state.track_pools:
    with st.spinner("Fetching songs from Spotify..."):
        st.session_state.track_pools[mood] = fetch_spotify_tracks(mood)
        st.session_state.track_indices[mood] = 0

tracks = st.session_state.track_pools[mood]
index = st.session_state.track_indices[mood]

# ---- Show 5 unique tracks every time ----
def get_next_five_tracks(tracks, index):
    if not tracks:
        return [], 0
    n = len(tracks)
    if index + 5 > n:
        # If we've reached the end, reshuffle and start over
        random.shuffle(tracks)
        index = 0
    return tracks[index:index+5], index + 5

if st.button("🔄 Refresh Songs") or "current_tracks" not in st.session_state or st.session_state.get("last_mood") != mood:
    # On refresh or mood change, get next 5 songs
    current_tracks, new_index = get_next_five_tracks(tracks, index)
    st.session_state.current_tracks = current_tracks
    st.session_state.track_indices[mood] = new_index
    st.session_state.last_mood = mood
else:
    current_tracks = st.session_state.get("current_tracks", [])

# ---- Display the songs ----
if current_tracks:
    for title, url in current_tracks:
        st.markdown(
            f"""
            <div class="song-card">
                <p><strong>Spotify Recommendation:</strong></p>
                <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.warning("No songs found for this mood. Try refreshing or selecting a different mood.")
