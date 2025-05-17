import streamlit as st
import pandas as pd
import numpy as np

# Set page layout
#st.set_page_config(page_title="🎬 Movie Ratings Explorer", layout="wide")

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

# Section 1: Line chart using st.line_chart
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

# Section 2: Top Rated Genres (Bar chart only)
st.subheader("🎯 Top Rated Genres (All Time)")

top_genres = (
    data[data['genres'].isin(selected_genres)]
    .groupby('genres')['rating']
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(top_genres)

# Section 3: What's Trending This Year
st.subheader("🔥 What’s Trending Now?")

latest_year = data['year'].max()
latest_data = data[data['year'] == latest_year]

trending = (
    latest_data.groupby('genres')['rating']
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(trending.head(5))