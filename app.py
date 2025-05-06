import streamlit as st
import random

# Inject CSS for animated gradient background and custom fonts
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

    /* Navigation bar styling */
    .nav-bar {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .nav-button {
        background-color: rgba(255, 255, 255, 0.2);
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.4);
    }

    /* Song card styling */
    .song-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .song-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    /* Responsive grid container */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }

    a {
        color: #FFD700;
        text-decoration: none;
        font-weight: 600;
    }

    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define music recommendations by mood
music_data = {
    "happy": [
        ("Tareefan - Veere Di Wedding", "https://www.youtube.com/watch?v=3SWc5G8Gx7E"),
        ("Morni Banke - Badhaai Ho", "https://www.youtube.com/watch?v=1EadhOBcfI0"),
        ("Laung Laachi - Laung Laachi", "https://www.youtube.com/watch?v=YpkJO_GrCo0"),
        ("Sauda Khara Khara - Good Newwz", "https://www.youtube.com/watch?v=LYEqeUr-158"),
        ("Dil Chori - Sonu Ke Titu Ki Sweety", "https://www.youtube.com/watch?v=xWi8nDUjHGA"),
        ("Lungi Dance - Chennai Express", "https://www.youtube.com/watch?v=69CEiHfS_mc"),
        ("Bolo Ta Ra Ra - Daler Mehndi", "https://www.youtube.com/watch?v=lhVceZE1lf4"),
        ("Tamma Tamma Again - Badrinath Ki Dulhania", "https://www.youtube.com/watch?v=EEX_XM6SxmY"),
        ("Coka - Sukh-E Muzical Doctorz", "https://www.youtube.com/watch?v=7lWeQs8Firo"),
        ("Kala Chashma - Baar Baar Dekho", "https://www.youtube.com/watch?v=4WRJHbL4dAk"),
    ],
    "sad": [
        ("Dildaar Tera - Sandeep Chandel, Rohit Sardhana", "https://www.youtube.com/watch?v=cSUhBp3jNJQ"),
        ("Nashe Pate - Mohit Sharma", "https://www.youtube.com/watch?v=oAzyZGa9ygE"),
        ("Dil Tut Gya - Diler Kharkiya", "https://www.youtube.com/watch?v=5jNexY8xrug"),
        ("Aashiqi Ka Rog - Diler Kharkiya", "https://www.youtube.com/watch?v=QgZupxYr-RA"),
        ("Kamaal Hai - Amit Dhull", "https://www.youtube.com/watch?v=przUl8E1WBY"),
        ("Channa Mereya - Arijit Singh", "https://www.youtube.com/watch?v=bzSTpdcs-EI"),
        ("Tum Hi Ho - Arijit Singh", "https://www.youtube.com/watch?v=Umqb9KENgmk"),
        ("Kabira - Pritam, Tochi Raina, Rekha Bhardwaj", "https://www.youtube.com/watch?v=jHNNMj5bNQw"),
        ("Tera Ban Jaunga - Akhil Sachdeva, Tulsi Kumar", "https://www.youtube.com/watch?v=Qdz5n1Xe5Qo"),
        ("Badmash Bolu Su - KD", "https://www.youtube.com/watch?v=Mk132xeCnMQ"),
    ],
    "energetic": [
        ("Goli - Diler Kharkiya", "https://www.youtube.com/watch?v=GMmkbU5b92Q"),
        ("Bhangra Paale - Gippy Grewal", "https://www.youtube.com/watch?v=WYa2qi0s9Ek"),
        ("Khadke Glassy - Yo Yo Honey Singh", "https://www.youtube.com/watch?v=AmrRPNwrGQU"),
        ("Chandigarh - Kaka", "https://www.youtube.com/watch?v=2DIU1SjTJB4"),
        ("Lungi Dance - Yo Yo Honey Singh", "https://www.youtube.com/watch?v=69CEiHfS_mc"),
        ("Morni Banke - Guru Randhawa, Neha Kakkar", "https://www.youtube.com/watch?v=1EadhOBcfI0"),
        ("Taki Taki - DJ Snake, Selena Gomez", "https://www.youtube.com/watch?v=ixkoVwKQaJg"),
        ("Kar Gayi Chull - Badshah, Neha Kakkar", "https://www.youtube.com/watch?v=NTHz9ephYTw"),
        ("Aankh Marey - Mika Singh", "https://www.youtube.com/watch?v=_KhQT-LGb-4"),
        ("Ghungroo - Arijit Singh, Shilpa Rao", "https://www.youtube.com/watch?v=qFkNATtc3mc"),
    ],
    "relaxed": [
        ("Tum Hi Ho - Aashiqui 2", "https://www.youtube.com/watch?v=Umqb9KENgmk"),
        ("Kabira - Yeh Jawaani Hai Deewani", "https://www.youtube.com/watch?v=jHNNMj5bNQw"),
        ("Dil Diyan Gallan - Tiger Zinda Hai", "https://www.youtube.com/watch?v=SAcpESN_Fk4"),
        ("Raabta - Agent Vinod", "https://www.youtube.com/watch?v=zlt38OOqwDc"),
        ("Khuda Jaane - Bachna Ae Haseeno", "https://www.youtube.com/watch?v=cmMiyZaSELo"),
        ("Jeene Laga Hoon - Ramaiya Vastavaiya", "https://www.youtube.com/watch?v=qpIdoaaPa6U"),
        ("Hasi Ban Gaye - Hamari Adhuri Kahani", "https://www.youtube.com/watch?v=FOkVXadnO88"),
        ("Tujhse Naraz Nahi Zindagi - Masoom", "https://www.youtube.com/watch?v=LZ_YUOr-tYw"),
        ("Tera Ban Jaunga - Kabir Singh", "https://www.youtube.com/watch?v=Qdz5n1Xe5Qo"),
        ("Tum Mile - Tum Mile", "https://www.youtube.com/watch?v=UcqI3uBKgTg"),
    ],
    "romantic": [
        ("Tere Bina - Arijit Singh", "https://www.youtube.com/watch?v=m05HDNnxLFk"),
        ("Kahani Suno - Kaifi Khalil", "https://www.youtube.com/watch?v=_XBVWlI8TsQ"),
        ("Yaad Teri - Raju Punjabi", "https://www.youtube.com/watch?v=ZQdA-7UrQRM"),
        ("Jine Laga Hu - Girish Kumar", "https://www.youtube.com/watch?v=wa"),
        ("Lilo Chaman - Diler Kharkiya", "https://www.youtube.com/watch?v=d7_Puc95qrc"),
        ("Aacha Lage Se - Raju Punjabi", "https://www.youtube.com/watch?v=veVOxTkKSMU"),
        ("Yaad Teri - Raju Punjabi", "https://www.youtube.com/watch?v=ZQdA-7UrQRM"),
        ("Tere Bina - Guru Randhawa", "https://www.youtube.com/watch?v=9JDSGhhiOwI"),
        ("Tujhe Kitna Chahne Lage - Kabir Singh", "https://www.youtube.com/watch?v=2IGDsD-dLF8"),
        ("Tum Se Hi - Jab We Met", "https://www.youtube.com/watch?v=Cb6wuzOurPc"),
    ],
}

# Title and description
st.title("🎵 Mood-Based Music Recommendation")
st.write(
    "Select your current mood and get personalized music recommendations to match your vibe."
)

# Mood selection
mood = st.selectbox(
    "Choose your mood:",
    options=list(music_data.keys()),
    index=0,
)

# Function to display recommendations
def display_recommendations(mood):
    songs = music_data.get(mood, [])
    if not songs:
        st.warning("No recommendations available for this mood.")
        return

    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    for title, url in songs:
        card_html = f"""
        <div class="song-card">
            <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Show recommendations
display_recommendations(mood)
