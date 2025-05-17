import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="🎬 Movie Ratings Explorer", layout="wide")

st.title("🎥 Movie Trends for Young Adults (18–35)")
st.markdown("Explore genre trends, top-rated movies, and what's hot right now. Tailored for online movie retail success!")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genres_expanded.csv")

data = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
genres = data['genres'].unique()
selected_genres = st.sidebar.multiselect("🎞️ Choose genres:", genres, default=genres)

min_year = int(data['year'].min())
max_year = int(data['year'].max())
selected_year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

# Filter data
filtered = data[
    (data['genres'].isin(selected_genres)) &
    (data['year'] >= selected_year_range[0]) &
    (data['year'] <= selected_year_range[1])
]

# Line Chart: Average Ratings Over Time
st.subheader("📈 Average Movie Ratings Over Time by Genre")

if not selected_genres:
    st.warning("Please select at least one genre to see the trend.")
else:
    avg_ratings = (
        filtered
        .groupby(['year', 'genres'])['rating']
        .mean()
        .reset_index()
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
        title={'text': '📈 Average Movie Ratings Over Time by Genre', 'x': 0.5, 'font': {'size': 30}},
        xaxis_title="Year",
        yaxis_title="Average Rating",
        font=dict(size=16),
        legend_title="Genre",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 🎯 Top Rated Genres (Overall)
# -----------------------------
st.subheader("🎯 Top Rated Genres (Overall)")

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
    bar_fig = px.bar(top_genres, x='genres', y='rating', color='genres',
                     title="Top Rated Genres", labels={'rating': 'Avg Rating'})
    bar_fig.update_layout(showlegend=False, font=dict(size=14), title_font_size=24)
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    st.markdown("**🥧 Pie Chart**")
    pie_fig = px.pie(top_genres, names='genres', values='rating', title="Top Rated Genres (Pie View)")
    pie_fig.update_layout(font=dict(size=14), title_font_size=24)
    st.plotly_chart(pie_fig, use_container_width=True)

# -----------------------------
# 🔥 What’s Trending?
# -----------------------------
st.subheader("🔥 What’s Trending? (Top Genres This Year)")

current_year = data['year'].max()
current_year_data = data[data['year'] == current_year]

trending = (
    current_year_data
    .groupby('genres')['rating']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

trend_fig = px.bar(trending.head(5), x='genres', y='rating', color='genres',
                   title=f"🔥 Top Genres in {current_year}", labels={'rating': 'Avg Rating'})
trend_fig.update_layout(showlegend=False, font=dict(size=14), title_font_size=26)
st.plotly_chart(trend_fig, use_container_width=True)

# Optional: raw data
with st.expander("🗂 Show Raw Filtered Data"):
    st.dataframe(filtered)