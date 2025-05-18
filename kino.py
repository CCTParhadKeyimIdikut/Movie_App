import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎥 Movie Ratings Explorer", layout="wide")

# Title and intro
st.title("🎥 Movie Ratings Explorer")
st.markdown("""
Explore genre trends, top-rated movies, and what's hot right now — perfect for understanding what young movie lovers enjoy.
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genres_expanded.csv")

data = load_data()

# Show raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data (First 100 Rows)')
    st.write(data.head(100))

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
genres = sorted(data['genres'].unique())
selected_genres = st.sidebar.multiselect("🎞️ Choose Genres", genres, default=['Drama'])

min_year = int(data['year'].min())
max_year = int(data['year'].max())
year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

# Filter dataset
filtered = data[
    (data['genres'].isin(selected_genres)) &
    (data['year'] >= year_range[0]) &
    (data['year'] <= year_range[1])
]

# Section 1: Line Chart — Ratings Over Time
st.subheader("📈 Average Movie Ratings Over Time by Genre")

if selected_genres:
    avg_ratings = filtered.groupby(['year', 'genres'])['rating'].mean().reset_index()
    fig_line = px.line(avg_ratings, x="year", y="rating", color="genres",
                       title="📈 Average Movie Ratings Over Time by Genre")
    fig_line.update_layout(title_font_size=24, font_size=14, yaxis_title='Average Rating', xaxis_title='Year')
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("Please select at least one genre to see the trend.")

# Section 2: Top Rated Genres (All Time)
st.subheader("🏆 Top Rated Genres (All Time)")

top_genres = (
    data.groupby('genres')['rating'].mean().reset_index()
    .sort_values(by='rating', ascending=False)
)
fig_top_genres = px.bar(top_genres, x='genres', y='rating',
                        title="🏆 Top Rated Genres (All Time)",
                        color='rating', color_continuous_scale='Viridis')
fig_top_genres.update_layout(xaxis_title='Genre', yaxis_title='Average Rating', title_font_size=24)
st.plotly_chart(fig_top_genres, use_container_width=True)

# Section 3: Top 10 Most Frequent Genres
st.subheader("📊 Top 10 Most Frequent Genres")

genre_counts = data['genres'].value_counts().reset_index().head(10)
genre_counts.columns = ['genres', 'count']
fig_freq_genres = px.bar(genre_counts, x='count', y='genres', orientation='h',
                         title='📊 Top 10 Most Frequent Genres',
                         color='count', color_continuous_scale='Purples')
fig_freq_genres.update_layout(xaxis_title='Count', yaxis_title='Genre',
                              yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_freq_genres, use_container_width=True)

# Section 4: Top Rated Movies (All Time)
st.subheader("🎬 Top Rated Movies (All Time)")

top_movies = (
    data[['title', 'rating']].drop_duplicates()
    .sort_values(by='rating', ascending=False).head(10)
)
fig_top_movies = px.bar(top_movies, x='rating', y='title', orientation='h',
                        title='🎬 Top Rated Movies (All Time)',
                        color='rating', color_continuous_scale='Greens')
fig_top_movies.update_layout(xaxis_title='Rating', yaxis_title='Movie Title',
                             yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_top_movies, use_container_width=True)

# Section 5: Top 10 Most Frequent Movies by Title
st.subheader("📺 Top 10 Most Frequent Movies by Title")

movie_counts = filtered['title'].value_counts().reset_index().head(10)
movie_counts.columns = ['title', 'count']
fig_freq_movies = px.bar(movie_counts, x='count', y='title', orientation='h',
                         title='📺 Top 10 Most Frequent Movies by Title',
                         color='count', color_continuous_scale='Cividis')
fig_freq_movies.update_layout(xaxis_title='Count', yaxis_title='Movie Title',
                              yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_freq_movies, use_container_width=True)

# Section 6: What’s Trending This Year
st.subheader("🔥 What’s Trending Now?")

latest_year = data['year'].max()
latest_data = data[data['year'] == latest_year]
trending = latest_data.groupby('genres')['rating'].mean().sort_values(ascending=False).head(5)

fig_trending = px.bar(trending, x=trending.values, y=trending.index, orientation='h',
                      title=f"🔥 Trending Genres in {latest_year}",
                      color=trending.values, color_continuous_scale='Oranges')
fig_trending.update_layout(xaxis_title='Average Rating', yaxis_title='Genre',
                           yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_trending, use_container_width=True)
