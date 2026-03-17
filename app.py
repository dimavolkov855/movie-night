import random
import requests
import streamlit as st

st.set_page_config(
    page_title="Movie Night Picker",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f1020 0%, #17182f 40%, #1d1135 100%);
    color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
    color: white;
}

.subtitle {
    font-size: 1.05rem;
    color: #c9cbe3;
    margin-bottom: 2rem;
}

.badge-row {
    display: flex;
    gap: 10px;
    margin-top: 0.3rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    background: rgba(255,255,255,0.08);
    color: #f4f6fb;
    border: 1px solid rgba(255,255,255,0.12);
}

.section-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    backdrop-filter: blur(8px);
}

.movie-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.2);
}

.movie-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.movie-meta {
    color: #d6daef;
    font-size: 0.95rem;
    margin-bottom: 0.75rem;
}

.movie-overview {
    color: #f3f5fb;
    line-height: 1.6;
    font-size: 1rem;
}

.result-header {
    font-size: 1.7rem;
    font-weight: 800;
    color: #ffffff;
    margin-top: 1.2rem;
    margin-bottom: 1rem;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
}

input {
    color: white !important;
}

label, .stSelectbox label, .stTextInput label {
    color: #eef1fb !important;
    font-weight: 600 !important;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 0.8rem 1rem;
    font-weight: 700;
    font-size: 1rem;
    color: white;
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.35);
    transition: 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 Movie Night Picker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Pick a mood, choose who you are watching with, and get stylish movie recommendations from TMDb.</div>',
    unsafe_allow_html=True
)

if "page" not in st.session_state:
    st.session_state.page = 1


def get_genre_filters(mood, group_type):
    if mood == "Funny":
        if group_type == "Date night":
            return {"include": "35,10749", "exclude": "27,99,10752,53"}
        elif group_type == "Family":
            return {"include": "35,10751", "exclude": "27,53,80,10752"}
        else:
            return {"include": "35", "exclude": "27,99,10752"}

    elif mood == "Cozy":
        if group_type == "Family":
            return {"include": "10751,16", "exclude": "27,53,80"}
        else:
            return {"include": "35,10749", "exclude": "27,53,80"}

    elif mood == "Tense":
        return {"include": "53,9648", "exclude": "16,10751,35"}

    elif mood == "Mind-blowing":
        return {"include": "878", "exclude": "27,10751"}

    elif mood == "Feel-good":
        return {"include": "35,10749", "exclude": "27,53,10752"}

    return {"include": "", "exclude": ""}


def score_movie(movie, mood, group_type):
    genres = movie.get("genre_ids", [])
    score = 0

    COMEDY = 35
    ROMANCE = 10749
    FAMILY = 10751
    HORROR = 27
    WAR = 10752
    THRILLER = 53
    CRIME = 80
    DOCUMENTARY = 99
    SCI_FI = 878
    MYSTERY = 9648
    ACTION = 28

    if mood == "Funny":
        if COMEDY in genres:
            score += 6
        if group_type == "Date night" and ROMANCE in genres:
            score += 3
        if FAMILY in genres and group_type != "Family":
            score -= 1
        if HORROR in genres:
            score -= 5
        if WAR in genres:
            score -= 4
        if THRILLER in genres:
            score -= 3
        if DOCUMENTARY in genres:
            score -= 4

    elif mood == "Cozy":
        if ROMANCE in genres:
            score += 3
        if COMEDY in genres:
            score += 3
        if FAMILY in genres:
            score += 2
        if HORROR in genres or THRILLER in genres or CRIME in genres:
            score -= 4

    elif mood == "Tense":
        if THRILLER in genres:
            score += 4
        if CRIME in genres:
            score += 2
        if MYSTERY in genres:
            score += 2
        if COMEDY in genres or FAMILY in genres:
            score -= 3

    elif mood == "Mind-blowing":
        if SCI_FI in genres:
            score += 4
        if MYSTERY in genres:
            score += 3
        if THRILLER in genres:
            score += 2
        if ACTION in genres:
            score += 1

    elif mood == "Feel-good":
        if COMEDY in genres:
            score += 4
        if FAMILY in genres:
            score += 2
        if ROMANCE in genres:
            score += 2
        if HORROR in genres or WAR in genres or THRILLER in genres:
            score -= 4

    return score


def get_movie_pool(mood, group_type, page=1):
    token = st.secrets["TMDB_BEARER_TOKEN"]
    url = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }

    genre_filters = get_genre_filters(mood, group_type)

    for _ in range(5):
        random_page = random.randint(1, 50)

        params = {
            "sort_by": "popularity.desc",
            "page": random_page,
            "vote_count.gte": 300,
            "include_adult": "false",
            "with_original_language": "en",
            "primary_release_date.lte": "2026-03-17",
            "with_genres": genre_filters["include"],
            "without_genres": genre_filters["exclude"],
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        movies = data.get("results", [])

        for min_score in [5, 4, 3, 2]:
            filtered_movies = [
                movie for movie in movies
                if score_movie(movie, mood, group_type) >= min_score
            ]
            if filtered_movies:
                return filtered_movies

    return []


def render_movie_card(movie):
    poster_path = movie.get("poster_path")
    title = movie.get("title", "Unknown title")
    release_date = movie.get("release_date", "Unknown")
    rating = movie.get("vote_average", "N/A")
    overview = movie.get("overview", "No overview available.")

    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2.3], vertical_alignment="top")

    with col1:
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            st.image(poster_url, use_container_width=True)
        else:
            st.markdown('<div class="badge">No poster</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="movie-meta">⭐ {rating} &nbsp;&nbsp;•&nbsp;&nbsp; 📅 {release_date}</div>',
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="movie-overview">{overview}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


left, right = st.columns(2)
with left:
    mood = st.selectbox(
        "Choose a mood",
        ["Funny", "Cozy", "Tense", "Mind-blowing", "Feel-good"]
    )
with right:
    group_type = st.selectbox(
        "Who are you watching with?",
        ["Solo", "Date night", "Friends", "Family"]
    )

preferences = st.text_input(
    "Any extra preferences?",
    placeholder="No horror, under 2 hours, not too sad"
)

st.markdown(
    f"""
    <div class="badge-row">
        <div class="badge">Mood: {mood}</div>
        <div class="badge">Group: {group_type}</div>
        <div class="badge">Preferences: {preferences if preferences else "None"}</div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    pick_clicked = st.button("Pick movies", use_container_width=True)

with col2:
    refresh_clicked = st.button("Refresh choices", use_container_width=True)

if pick_clicked:
    st.session_state.page = random.randint(1, 50)

if refresh_clicked:
    st.session_state.page = random.randint(1, 50)

if pick_clicked or refresh_clicked:
    movies = get_movie_pool(mood, group_type, st.session_state.page)

    movies = sorted(
        movies,
        key=lambda movie: movie.get("vote_average", 0),
        reverse=True
    )

    st.markdown('<div class="result-header">Your movie picks</div>', unsafe_allow_html=True)

    if not movies:
        st.warning("No good matches found. Try Refresh choices.")
    else:
        for movie in movies[:5]:
            render_movie_card(movie)