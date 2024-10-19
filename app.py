import streamlit as st
import pandas as pd
import plotly.express as px
import os
import kagglehub

# Set up the page configuration
st.set_page_config(page_title='Spotify Top Streams 2023 Dashboard', layout='wide')

# Title and description
st.title('🎵 Spotify Top Streams 2023 Dashboard')
st.markdown('An interactive dashboard analyzing the top streamed tracks on Spotify in 2023.')

# Function to initialize Kaggle API
def init_kaggle_api():
    os.environ['KAGGLE_USERNAME'] = st.secrets['KAGGLE_USERNAME']
    os.environ['KAGGLE_KEY'] = st.secrets['KAGGLE_KEY']


# Function to load data from KaggleHub
# Initialize KaggleHub and download dataset
@st.cache_data
def load_data():
    # Download the dataset and specify the path
    path = kagglehub.dataset_download("rajatsurana979/most-streamed-spotify-songs-2023")
    
    # Dataset file
    dataset_file = 'spotify-2023.csv'
    data_file_path = f'{path}/{dataset_file}'

    # Read the dataset
    df = pd.read_csv(data_file_path, encoding='latin1')
    return df
    
# Load the data
df = load_data()

# Preprocess the data
df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]

# Sidebar filters
st.sidebar.title('Filters')

# Artist filter
all_artists = df['artist(s)'].str.split(', ').explode().unique()
selected_artists = st.sidebar.multiselect('Select Artist(s)', options=all_artists, default=all_artists)

# Filter DataFrame based on selected artists
df_filtered = df[df['artist(s)'].str.contains('|'.join(selected_artists))]

# Visualization 1: Top Tracks by Streams
st.markdown('## Top Tracks by Streams')
top_tracks = df_filtered.sort_values('streams', ascending=False)

fig1 = px.bar(
    top_tracks,
    x='streams',
    y='track_name',
    orientation='h',
    color='streams',
    color_continuous_scale='Viridis',
    title='Top Tracks by Streams',
    labels={'streams': 'Streams', 'track_name': 'Track Name'},
    height=600
)
fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Number of Top Tracks per Artist
st.markdown('## Number of Top Tracks per Artist')
artist_list = df_filtered['artist(s)'].str.split(', ')
artists = artist_list.explode()
artist_counts = artists.value_counts().reset_index()
artist_counts.columns = ['artist_name', 'count']

fig2 = px.bar(
    artist_counts.sort_values('count', ascending=True),
    x='count',
    y='artist_name',
    orientation='h',
    color='count',
    color_continuous_scale='Plasma',
    title='Number of Top Tracks per Artist',
    labels={'count': 'Number of Tracks', 'artist_name': 'Artist Name'},
    height=600
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Danceability vs Energy
st.markdown('## Danceability vs Energy')
if 'danceability' in df_filtered.columns and 'energy' in df_filtered.columns:
    fig3 = px.scatter(
        df_filtered,
        x='danceability',
        y='energy',
        size='streams',
        color='track_name',
        hover_data=['artist(s)'],
        title='Danceability vs Energy',
        labels={'danceability': 'Danceability', 'energy': 'Energy'},
        height=600
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning('Danceability and Energy data are not available in the dataset.')

# Visualization 4: Correlation Heatmap
st.markdown('## Correlation Heatmap')
numeric_cols = ['streams', 'danceability', 'valence', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']
numeric_cols = [col for col in numeric_cols if col in df_filtered.columns]
if numeric_cols:
    corr = df_filtered[numeric_cols].corr()

    fig4 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title='Correlation Heatmap',
        labels=dict(color='Correlation Coefficient'),
        height=600
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning('Not enough numeric data available for correlation heatmap.')
