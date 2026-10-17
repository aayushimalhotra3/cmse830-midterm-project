# Why Does This Song Feel Like That?

This is my midterm project for CMSE 830. It's a Streamlit app that lets you explore songs by their mood and find music that matches a vibe.

The idea is that a lot of people pick music by how it feels but can't really say what makes a song sound happy, sad, chill or hyped. This app uses two of Spotify's audio features, valence (how positive a song sounds) and energy (how intense it is), to sort songs into moods and let you explore them.

## The data

I'm using the 30,000 Spotify Songs dataset (from Kaggle / TidyTuesday). It has about 32,833 rows and 23 columns, where one row is a song as it appears in a playlist. The audio features like valence, energy and danceability come from Spotify's API. The CSV is included in this repo under `spotify_dataset/`.

## What the app does right now

- sorts songs into four moods using valence and energy (happy/energetic, chill/content, angry/tense, sad/mellow)
- lets you pick a mood, filter by genre, and set a max popularity to find more hidden gems
- shows an interactive mood map (valence vs energy) of the songs that match
- shows a table of the matching songs, kind of like a playlist

## How to run it locally

1. clone this repo
2. install the packages:
   ```
   pip install -r requirements.txt
   ```
3. run the app from the project folder:
   ```
   streamlit run app.py
   ```
4. it opens in your browser at http://localhost:8501

The app reads the data from `spotify_dataset/spotify_songs.csv`, so run it from the project folder so the path works.

## Files

- `app.py` - the Streamlit app
- `eda.ipynb` - my exploratory data analysis
- `eda_extended.ipynb` - extra EDA (mood groups, correlations)
- `spotify_dataset/` - the dataset
- `requirements.txt` - packages needed

## Limitations

- mood is inferred from valence and energy, it's not how people actually feel about a song
- genre comes from the playlist a song was on, not an official genre label
- the same song can show up in more than one playlist, so I use unique songs for the analysis

## Note

This is still in progress for the midterm, I'll keep improving the app before the presentation.

## AI use

I used AI (Claude) to help with Streamlit syntax, debugging, and organizing this repo. I ran and tested all the code myself, and the project question, data decisions, and interpretations are my own.
