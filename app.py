import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Why does this song feel like that?", page_icon="🎵", layout="wide")

# load data, keep each song once
@st.cache_data
def load_data():
    df = pd.read_csv("spotify_dataset/spotify_songs.csv")
    df = df.drop_duplicates("track_id")

    # split into 4 moods by valence and energy
    def get_mood(row):
        if row["valence"] >= 0.5 and row["energy"] >= 0.5:
            return "Happy / Energetic"
        elif row["valence"] >= 0.5:
            return "Chill / Content"
        elif row["energy"] >= 0.5:
            return "Angry / Tense"
        else:
            return "Sad / Mellow"

    df["mood"] = df.apply(get_mood, axis=1)
    return df

df = load_data()

mood_colors = {
    "Happy / Energetic": "#F6B93B",
    "Chill / Content": "#60A3BC",
    "Angry / Tense": "#E55039",
    "Sad / Mellow": "#786FA6",
}

st.title("🎵 Why does this song feel like that?")
st.write(
    "Pick a mood and a genre and find songs that match the vibe. "
    "Mood comes from each song's **valence** (how positive it sounds) and **energy** (how intense it is)."
)

# controls
st.sidebar.header("Find your vibe")
mood = st.sidebar.selectbox("Mood", ["Any"] + list(mood_colors.keys()))
genres = st.sidebar.multiselect(
    "Genre",
    sorted(df["playlist_genre"].unique()),
    default=sorted(df["playlist_genre"].unique()),
)
max_pop = st.sidebar.slider("Max popularity (lower = more hidden gems)", 0, 100, 100)

# filter on what they picked
picked = df[df["playlist_genre"].isin(genres)]
if mood != "Any":
    picked = picked[picked["mood"] == mood]
picked = picked[picked["track_popularity"] <= max_pop]

st.subheader(f"{len(picked)} songs match your vibe")

if len(picked) == 0:
    st.warning("No songs match. Try widening the genres or raising the popularity.")
else:
    # sample so the plot isnt slow
    plot_df = picked.sample(min(len(picked), 2500), random_state=1)
    fig = px.scatter(
        plot_df,
        x="valence",
        y="energy",
        color="mood",
        color_discrete_map=mood_colors,
        hover_data=["track_name", "track_artist", "playlist_genre"],
        title="Mood map of your songs",
    )
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
    fig.add_vline(x=0.5, line_dash="dash", line_color="gray")
    fig.update_layout(
        xaxis_title="valence (sad → happy)",
        yaxis_title="energy (calm → intense)",
        xaxis_range=[0, 1],
        yaxis_range=[0, 1],
    )
    st.plotly_chart(fig, use_container_width=True)

    # matching songs as a playlist
    st.subheader("Your playlist")
    playlist = (
        picked[["track_name", "track_artist", "playlist_genre", "mood", "track_popularity"]]
        .sort_values("track_popularity", ascending=False)
        .head(50)
        .reset_index(drop=True)
    )
    st.dataframe(playlist, use_container_width=True)
