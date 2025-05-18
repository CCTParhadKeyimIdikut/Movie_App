import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="🎥 Movie Ratings Explorer", layout="centered")

st.title("🎥 Movie Ratings Explorer")
st.markdown("""
Explore genre trends, top-rated and the most frequent movies. """)

@st.cache_data
def load_data():
    df = pd.read_csv("genres_expanded.csv")
    return df

data = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Raw data (First 100 Rows)')
    st.write(data.head(100))

st.sidebar.header("🔍 Filter Options")
genres = sorted(data['genres'].unique())
selected_genres = st.sidebar.multiselect("🎞️ Choose Genres", genres, default=genres)

min_year = int(data['year'].min())
max_year = int(data['year'].max())
year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

filtered = data[
    (data['genres'].isin(selected_genres)) &
    (data['year'] >= year_range[0]) &
    (data['year'] <= year_range[1])
]

# Line chart
st.subheader("📈 Average Movie Ratings Over Time by Genre")

if selected_genres:
    avg_ratings = (
        filtered.groupby(['year', 'genres'])['rating']
        .mean().reset_index())

    line_chart = alt.Chart(avg_ratings).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('rating:Q', title='Average Rating'),
        color=alt.Color('genres:N', title='Genre', scale=alt.Scale(scheme='tableau10'))
    ).properties(
        width=700,height=400
    )

    st.altair_chart(line_chart)
else:
    st.warning("Please select at least one genre to see the trend.")

# Top Rated Genres (All Time)
st.subheader("🎯 Top Rated Genres (All Time)")

top_genres_df = (
    data[data['genres'].isin(selected_genres)].groupby('genres')['rating'].mean()
    .reset_index()
    .sort_values(by='rating', ascending=False)
)

top_genres_chart = alt.Chart(top_genres_df).mark_bar(color='#f39c12').encode(
    x=alt.X('genres:N', sort='-y', title='Genre'),
    y=alt.Y('rating:Q', title='Average Rating')
).properties(
    width=700,height=400,
    title='Top Rated Genres (All Time)'
)

st.altair_chart(top_genres_chart)

#Top 10 Most Frequent Genres
st.subheader("📊 Top 10 Most Frequent Genres")

genre_counts = data['genres'].value_counts().reset_index().head(10)
genre_counts.columns = ['genres', 'count']

freq_genre_chart = alt.Chart(genre_counts).mark_bar(color='#8e44ad').encode(
    x=alt.X('count:Q', title='Count'),
    y=alt.Y('genres:N', sort='-x', title='Genre')
).properties(
    width=700,height=400
)

st.altair_chart(freq_genre_chart)

# Section 4: Top Rated Movies by Title
st.subheader("🎬 Top Rated Movies (All Time)")

top_movies = (
    data[['title', 'rating']].drop_duplicates().sort_values(by='rating', ascending=False)
    .head(10)
)

top_movies_chart = alt.Chart(top_movies).mark_bar(color='#27ae60').encode(
    x=alt.X('rating:Q', title='Rating'),
    y=alt.Y('title:N', sort='-x', title='Movie Title')
).properties(
    width=700,height=400
)

st.altair_chart(top_movies_chart)

# Section 5: Top 10 Most Frequent Movies by Title
st.subheader("📺 Top 10 Most Frequent Movies by Title")

movie_counts = filtered['title'].value_counts().reset_index().head(10)
movie_counts.columns = ['title', 'count']

freq_movies_chart = alt.Chart(movie_counts).mark_bar(color='#6c5ce7').encode(
    x=alt.X('count:Q', title='Count'),
    y=alt.Y('title:N', sort='-x', title='Movie Title')
).properties(
    width=700,height=400
)

st.altair_chart(freq_movies_chart)