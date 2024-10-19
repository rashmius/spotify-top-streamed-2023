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
    path = kagglehub.dataset_download("rajatsurana979/most-streamed-spotify-songs-2023", path='spotify-2023.csv')
    
    # Dataset file
    dataset_file = 'spotify-2023.csv'
    data_file_path = f'{path}/{dataset_file}'

    # Read the dataset
    df = pd.read_csv(data_file_path, encoding='latin1')
    return df
    
# Load the data
df = load_data()

# Rest of your app code remains the same...
