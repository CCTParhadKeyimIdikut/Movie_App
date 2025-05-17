import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="🎬 Movie Ratings Explorer", layout="wide")

st.title("🎥 Movie Trends for Young Adults (18–35)")
st.markdown("""
Explore genre trends, top-rated movies, and what's hot right now — perfect for understanding what young movie lovers enjoy.
""")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("genres_expanded.csv")

data = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
genres = sorted(data['genres'].unique())
selected_genres = st.sidebar.multiselect("🎞️ Choose Genres", genres, default=genres)

min_year = int(data['year'].min())
max_year = int(data['year'].max())
year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

# Filter data
filtered = data[
    (data['genres'].isin(selected_genres)) &
    (data['year'] >= year_range[0]) &
    (data['year'] <= year_range[1])
]

# Section 1: Line Chart — Ratings Over Time
st.subheader("📈 Average Movie Ratings Over Time by Genre")

if selected_genres:
    avg_ratings = (
        filtered.groupby(['year', 'genres'])['rating']
        .mean().reset_index()
    )

    fig = px.line(
        avg_ratings,
        x='year',
        y='rating',
        color='genres',
        title='📈 Average Movie Ratings Over Time by Genre',
        markers=True
    )

    fig.update_layout(
        title={'text': '📈 Average Movie Ratings Over Time by Genre', 'x': 0.5, 'font': {'size': 28}},
        xaxis_title="Year",
        yaxis_title="Average Rating",
        font=dict(size=15),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one genre to see the trend.")

# Section 2: Top Rated Genres — Bar & Pie Chart
st.subheader("🎯 Top Rated Genres (All Time)")

top_genres = (
    data[data['genres'].isin(selected_genres)]
    .groupby('genres')['rating']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Bar Chart**")
    bar_fig = px.bar(
        top_genres,
        x='genres',
        y='rating',
        color='genres',
        title="Top Rated Genres (Bar Chart)",
        labels={'rating': 'Avg Rating'}
    )
    bar_fig.update_layout(showlegend=False, font=dict(size=14), title_font_size=22)
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    st