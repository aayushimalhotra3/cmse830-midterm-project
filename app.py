import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Why does this song feel like that?", page_icon="🎵", layout="wide")

# load data and keep each song once
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
    df["year"] = pd.to_datetime(df["track_album_release_date"], errors="coerce").dt.year
    return df.reset_index(drop=True)

df = load_data()

# scale the feel features so one big one doesnt take over
@st.cache_data
def feel_matrix(data):
    feats = ["valence", "energy", "danceability", "acousticness", "loudness", "tempo", "speechiness"]
    x = data[feats]
    return (x - x.mean()) / x.std()

feel = feel_matrix(df)

# find the closest songs by their audio features
def similar_songs(i, k=8, same_genre=False):
    dist = (((feel - feel.loc[i]) ** 2).sum(axis=1)) ** 0.5
    out = df.loc[dist.sort_values().index].copy()
    out["distance"] = dist.sort_values().values
    out = out[out["track_name"] != df.loc[i, "track_name"]]  # drop other copies of the same song
    if same_genre:
        out = out[out["playlist_genre"] == df.loc[i, "playlist_genre"]]
    # turn the distance into a match score out of 100
    scale = dist.median()
    out["match %"] = (100 * scale / (scale + out["distance"])).round().astype(int)
    return out.head(k)

mood_colors = {
    "Happy / Energetic": "#F6B93B",
    "Chill / Content": "#60A3BC",
    "Angry / Tense": "#E55039",
    "Sad / Mellow": "#786FA6",
}

# make the charts blend with the page
def prettify(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ECECEC"),
        margin=dict(l=10, r=10, t=55, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="#2A2A33")
    fig.update_yaxes(gridcolor="#2A2A33")
    return fig

st.title("Why does this song feel like that?")
st.caption("Find music by how it feels, not by genre or popularity.")

with st.expander("how are moods defined?"):
    st.write(
        "spotify scores each song on valence (0 = sad, 1 = happy) and energy (0 = calm, 1 = intense). "
        "i split both at 0.5 to get four moods: happy/energetic, chill/content, angry/tense, sad/mellow."
    )

tab1, tab2, tab3 = st.tabs(["Find your vibe", "How mood changed over time", "Find similar songs"])

# discovery tab
with tab1:
    c1, c2 = st.columns([1, 2])
    mood = c1.selectbox("Mood", ["Any"] + list(mood_colors.keys()))
    genres = c2.multiselect(
        "Genre",
        sorted(df["playlist_genre"].unique()),
        default=sorted(df["playlist_genre"].unique()),
    )
    max_pop = st.slider("Max popularity (lower = more hidden gems)", 0, 100, 100)

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
        fig.update_traces(marker=dict(size=6, opacity=0.65))
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray")

        # shade the four mood corners, labels live in the legend
        quads = [
            (0.5, 1, 0.5, 1, "#F6B93B"),
            (0, 0.5, 0.5, 1, "#E55039"),
            (0.5, 1, 0, 0.5, "#60A3BC"),
            (0, 0.5, 0, 0.5, "#786FA6"),
        ]
        for x0, x1, y0, y1, color in quads:
            fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                          fillcolor=color, opacity=0.10, line_width=0, layer="below")

        fig.update_layout(
            xaxis_title="valence (sad → happy)",
            yaxis_title="energy (calm → intense)",
            xaxis_range=[0, 1],
            yaxis_range=[0, 1],
        )
        st.plotly_chart(prettify(fig), use_container_width=True)
        st.caption("popularity barely tracks any audio feature, so lower the max popularity to find hidden gems that feel just like the hits")

        # matching songs as a playlist
        st.subheader("Your playlist")
        playlist = (
            picked[["track_name", "track_artist", "playlist_genre", "mood", "track_popularity"]]
            .sort_values("track_popularity", ascending=False)
            .head(50)
            .reset_index(drop=True)
        )
        st.dataframe(playlist, use_container_width=True)

# mood over time tab
with tab2:
    st.subheader("Music got sadder after ~2013, but stayed just as energetic")

    timed = df.dropna(subset=["year"])
    timed = timed[(timed["year"] >= 1990) & (timed["year"] <= 2020)]

    yr = st.slider("Year range", 1990, 2020, (1990, 2020))
    timed = timed[(timed["year"] >= yr[0]) & (timed["year"] <= yr[1])]

    by_year = (
        timed.groupby("year")
        .agg(valence=("valence", "mean"), energy=("energy", "mean"), songs=("track_id", "size"))
        .reset_index()
    )
    # only years with enough songs
    by_year = by_year[by_year["songs"] >= 100]

    line = px.line(
        by_year,
        x="year",
        y=["valence", "energy"],
        markers=True,
        color_discrete_map={"valence": "#F6B93B", "energy": "#E55039"},
        title="Average valence and energy by release year",
    )
    line.update_layout(yaxis_title="average (0-1)", xaxis_title="release year", yaxis_range=[0.3, 0.85])
    st.plotly_chart(prettify(line), use_container_width=True)
    st.caption("only years with at least 100 songs are shown, the data is heaviest in the 2010s")

# find similar songs tab
with tab3:
    st.subheader("Find songs that feel like another song")
    st.caption("Pick a song and get the closest matches by how they actually sound, genre aside.")

    with st.expander("how this works"):
        st.write(
            "each song is compared on valence, energy, danceability, acousticness, loudness, tempo and "
            "speechiness. it ignores genre on purpose, and unlike a normal song radio it shows you why: "
            "the match % and the feature bars tell you how close each one really is."
        )

    # only pick from well known songs so the lists arent huge
    pool = df[df["track_popularity"] >= 60].dropna(subset=["track_name", "track_artist"]).copy()

    # pick an artist first then one of their songs
    artist = st.selectbox("Artist", sorted(pool["track_artist"].unique()))
    their_songs = pool[pool["track_artist"] == artist]
    song = st.selectbox("Song", sorted(their_songs["track_name"].unique()))
    same_genre = st.checkbox("only show songs from the same genre")
    seed = their_songs[their_songs["track_name"] == song].iloc[0]

    st.write(f"**{seed['track_name']}** by {seed['track_artist']} ({seed['playlist_genre']}) is {seed['mood']}.")
    st.caption(f"valence {seed['valence']:.2f} · energy {seed['energy']:.2f} · danceability {seed['danceability']:.2f}")

    near = similar_songs(seed.name, same_genre=same_genre)

    # plot the picked song and its matches and fade the rest out
    bg = df.sample(1500, random_state=1).assign(role="all songs", size=4)
    nb = near.assign(role="similar", size=9)
    sd = df.loc[[seed.name]].assign(role="your song", size=16)
    plot = pd.concat([bg, nb, sd])
    fig = px.scatter(
        plot,
        x="valence",
        y="energy",
        color="role",
        size="size",
        size_max=16,
        color_discrete_map={"all songs": "#D9D9D9", "similar": "#F6B93B", "your song": "#E55039"},
        hover_data=["track_name", "track_artist", "playlist_genre"],
        title="your song and its closest matches on the mood map",
    )
    fig.update_layout(xaxis_title="valence (sad → happy)", yaxis_title="energy (calm → intense)",
                      xaxis_range=[0, 1], yaxis_range=[0, 1])
    st.plotly_chart(prettify(fig), use_container_width=True)

    st.write("songs that feel the closest:")
    cols = ["match %", "track_name", "track_artist", "playlist_genre", "mood", "valence", "energy", "danceability"]
    st.dataframe(near[cols].reset_index(drop=True), use_container_width=True)

    # show why the top match lines up feature by feature
    top = near.iloc[0]
    show = ["valence", "energy", "danceability", "acousticness"]
    comp = pd.DataFrame({
        "feature": show + show,
        "song": ["your song"] * 4 + ["top match"] * 4,
        "score": [seed[f] for f in show] + [top[f] for f in show],
    })
    why = px.bar(
        comp,
        x="feature",
        y="score",
        color="song",
        barmode="group",
        color_discrete_map={"your song": "#E55039", "top match": "#F6B93B"},
        title=f"why '{top['track_name']}' is the closest match",
    )
    why.update_layout(yaxis_range=[0, 1])
    st.plotly_chart(prettify(why), use_container_width=True)

# limitations
with st.expander("Limitations"):
    st.write(
        "- mood is inferred from valence and energy, not how people actually feel about a song\n"
        "- genre comes from the playlist a song was on, not an official label\n"
        "- the same song can show up in multiple playlists so i use unique songs\n"
        "- the data is mostly 2010s so older years are less reliable\n"
        "- the similar songs are just the closest ones by audio features, not a trained recommender"
    )