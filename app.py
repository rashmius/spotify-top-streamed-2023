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

# Initialize KaggleHub
def init_kagglehub():
    client = kagglehub.Client()
    return client

# Function to load data from KaggleHub
@st.cache_data
def load_data():
    client = init_kagglehub()
    # Dataset details
    dataset = 'rajatsurana979/most-streamed-spotify-songs-2023'
    dataset_file = 'Data-Combined.csv'  # Using the combined dataset for more features

    # Download and load the dataset using KaggleHub
    dataset_dir = client.datasets.download(dataset)
    data_file_path = os.path.join(dataset_dir, dataset_file)

    # Read the dataset
    df = pd.read_csv(data_file_path, encoding='latin1')
    return df

# Load the data
df = load_data()

# Rest of your app code remains the same...
