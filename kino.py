import streamlit as st
import pandas as pd
import numpy as np

st.title("🎥 Movie Ratings Explorer")
st.markdown("""
Explore genre trends, top-rated movies, and what's hot right now — perfect for understanding what young movie lovers enjoy.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("genres_expanded.csv")
    return df

data = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Raw data (First 100 Rows)')
    st.write(data.head(100))

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
genres = sorted(data['genres'].unique())
selected_genres = st.sidebar.multiselect("🎞️ Choose Genres", genres, default=genres)

min_year = int(data['year'].min())
max_year = int(data['year'].max())
year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

# Filter dataset
filtered = data[
    (data['genres'].isin(selected_genres)) &
    (data['year'] >= year_range[0]) &
    (data['year'] <= year_range[1])
]

# Section 1: Line chart
st.subheader("📈 Average Movie Ratings Over Time by Genre")

if selected_genres:
    avg_ratings = (
        filtered.groupby(['year', 'genres'])['rating']
        .mean().reset_index()
    )
    pivot = avg_ratings.pivot(index='year', columns='genres', values='rating').fillna(0)
    st.line_chart(pivot)
else:
    st.warning("Please select at least one genre to see the trend.")

# Section 2: Top Rated Genres
st.subheader("🎯 Top Rated Genres (All Time)")

top_genres = (
    data[data['genres'].isin(selected_genres)]
    .groupby('genres')['rating']
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(top_genres)

# Section 3: Top 10 Most Frequent Genres
st.subheader("📊 Top 10 Most Frequent Genres")

genre_counts = data['genres'].value_counts().head(10)
genre_df = pd.DataFrame({'Genre': genre_counts.index, 'Count': genre_counts.values}).set_index('Genre')

st.bar_chart(genre_df)

# Section 4: Top Rated Movies (All Time)
st.subheader("🎬 Top Rated Movies (All Time)")

top_movies = (
    data[['title', 'rating']].drop_duplicates()
    .sort_values(by='rating', ascending=False).head(10)
).set_index('title')

st.bar_chart(top_movies)

# Section 5: Top 10 Most Frequent Movie Titles
st.subheader("📺 Top 10 Most Frequent Movies by Title")

movie_counts = filtered['title'].value_counts().head(10)
movie_df = pd.DataFrame({'Title': movie_counts.index, 'Count': movie_counts.values}).set_index('Title')

st.bar_chart(movie_df)
