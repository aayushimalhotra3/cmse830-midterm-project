# Why Does This Song Feel Like That?

This is my midterm project for CMSE 830. It's a Streamlit app for exploring songs by how they feel and finding music that matches a vibe.

The idea is that genre and popularity are actually pretty weak guides to how a song feels, so this app uses mood instead. Mood comes from two Spotify audio features, valence (how positive a song sounds) and energy (how intense it is), and those sort songs into four groups so you can explore music by feel.

## The data

I used the 30,000 Spotify Songs dataset from Kaggle. It's about 32833 rows and 23 columns where one row is a song as it appears in a playlist. The audio features like valence, energy and danceability come from Spotify's API. The CSV is in this repo under spotify_dataset.

## What the app does

There are three tabs:

- Find your vibe. Pick a mood, filter by genre, and set a max popularity to find hidden gems. Shows an interactive mood map and a playlist table of the matches.
- How mood changed over time. Music got sadder after about 2013 while staying just as energetic. A year slider lets you explore it.
- Find similar songs. Pick any song and get the closest matches by how they actually sound. It ignores genre on purpose and shows a match percent plus a little chart of why the top match fits.

## How to run it

1. clone this repo
2. install the packages
   ```
   pip install -r requirements.txt
   ```
3. run the app from the project folder
   ```
   streamlit run app.py
   ```
4. it opens at http://localhost:8501

The app reads the data from spotify_dataset/spotify_songs.csv, so run it from the project folder so the path works.

## Files

- app.py is the Streamlit app
- eda.ipynb is my exploratory data analysis
- spotify_dataset/ is the dataset
- requirements.txt is the packages needed
- .streamlit/config.toml is the app theme

## Limitations

- mood is inferred from valence and energy, not how people actually feel about a song
- genre comes from the playlist a song was on, not an official label
- the same song can show up in multiple playlists so i use unique songs
- the similar songs are just the closest ones by audio features, not a trained recommender
- the data is mostly 2010s so older years are less reliable

## AI use

I directed this project and made all the decisions. I chose the question, the data approach, and the app design, and I interpreted the findings myself. I used AI (Claude and ChatGPT) to help write and debug the code and build the app features. I ran and tested everything, and I can explain all of it.