# Why Does This Song Feel Like That?

this is my midterm project for cmse 830. its a streamlit app for exploring songs by how they feel and finding music that matches a vibe.

the idea is that genre and popularity are actually pretty weak guides to how a song feels so this app uses mood instead. mood comes from two spotify audio features valence (how positive a song sounds) and energy (how intense it is) and those sort songs into four groups so you can explore music by feel.

## the data

i used the 30,000 spotify songs dataset from kaggle. its about 32833 rows and 23 columns where one row is a song as it appears in a playlist. the audio features like valence energy and danceability come from spotifys api. the csv is in this repo under spotify_dataset.

## what the app does

there are three tabs:

- find your vibe. pick a mood filter by genre and set a max popularity to find hidden gems. shows an interactive mood map and a playlist table of the matches
- how mood changed over time. music got sadder after about 2013 while staying just as energetic. a year slider lets you explore it
- find similar songs. pick any song and get the closest matches by how they actually sound. it ignores genre on purpose and shows a match percent plus a little chart of why the top match fits

## how to run it

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

the app reads the data from spotify_dataset/spotify_songs.csv so run it from the project folder so the path works.

## files

- app.py is the streamlit app
- eda.ipynb is my exploratory data analysis
- spotify_dataset/ is the dataset
- requirements.txt is the packages needed
- .streamlit/config.toml is the app theme

## limitations

- mood is inferred from valence and energy not how people actually feel about a song
- genre comes from the playlist a song was on not an official label
- the same song can show up in multiple playlists so i use unique songs
- the similar songs are just the closest ones by audio features not a trained recommender
- the data is mostly 2010s so older years are less reliable

## ai use

i used ai (claude and chatgpt) to help build the app features write and debug code work through the analysis and organize the repo. i directed the project made the decisions ran and tested everything myself and i can explain all of it. the project question and the data choices are my own.
