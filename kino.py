import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

fig1, ax1 = plt.subplots()
top_genres.plot(kind='bar', color='green', ax=ax1)
ax1.set_ylabel("Average Rating")
ax1.set_title("Top Rated Genres")
st.pyplot(fig1)

# Section 3: Top 10 Most Frequent Genres
st.subheader("📊 Top 10 Most Frequent Genres")

genre_counts = data['genres'].value_counts().head(10)

fig2, ax2 = plt.subplots()
genre_counts.plot(kind='barh', color='purple', ax=ax2)
ax2.set_xlabel("Count")
ax2.set_ylabel("Genre")
ax2.set_title("Top 10 Most Frequent Genres")
st.pyplot(fig2)

# Section 4: Top Rated Movies (All Time)
st.subheader("🎬 Top Rated Movies (All Time)")

top_movies = (
    data[['title', 'rating']].drop_duplicates()
    .sort_values(by='rating', ascending=False).head(10)
).set_index('title')

fig3, ax3 = plt.subplots()
top_movies.plot(kind='barh', color='orange', ax=ax3, legend=False)
ax3.set_xlabel("Rating")
ax3.set_title("Top Rated Movies (All Time)")
ax3.invert_yaxis()
st.pyplot(fig3)

# Section 5: Top 10 Most Frequent Movie Titles
st.subheader("📺 Top 10 Most Frequent Movies by Title")

movie_counts = filtered['title'].value_counts().head(10)

fig4, ax4 = plt.subplots()
movie_counts.plot(kind='barh', color='red', ax=ax4)
ax4.set_xlabel("Count")
ax4.set_ylabel("Movie Title")
ax4.set_title("Top 10 Most Frequent Movies")
ax4.invert_yaxis()
st.pyplot(fig4)
