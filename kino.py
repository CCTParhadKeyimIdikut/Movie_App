import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎥 Movie Ratings Explorer", layout="wide")

st.title("🎥 Movie Ratings Explorer")
st.markdown("Explore genre trends, top-rated movies, and what's trending now — perfect for understanding what young movie lovers enjoy.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genres_expanded.csv")

data = load_data()

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

if st.checkbox('Show raw data'):
    st.subheader('Raw Data (First 100 Rows)')
    st.write(data.head(100))

# Section 1: Average Movie Ratings Over Time by Genre
st.subheader("📈 Average Movie Ratings Over Time by Genre")
if not selected_genres:
    st.warning("Please select at least one genre.")
else:
    avg_ratings = filtered.groupby(['year', 'genres'])['rating'].mean().reset_index()
    fig = px.line(avg_ratings, x="year", y="rating", color="genres",
                  title="📈 Average Movie Ratings Over Time by Genre")
