import streamlit as st
import pandas as pd
import plotly.express as px
import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Set up the page configuration
st.set_page_config(page_title='Spotify Top Streams 2023 Dashboard', layout='wide')

# Title and description
st.title('🎵 Spotify Top Streams 2023 Dashboard')
st.markdown('An interactive dashboard analyzing the top streamed tracks on Spotify in 2023.')

# Function to initialize Kaggle API
def init_kaggle_api():
    os.environ['KAGGLE_USERNAME'] = st.secrets['KAGGLE_USERNAME']
    os.environ['KAGGLE_KEY'] = st.secrets['KAGGLE_KEY']
    api = KaggleApi()
    api.authenticate()
    return api

# Function to load data from Kaggle
@st.cache_data
def load_data():
    api = init_kaggle_api()
    # Dataset details
    dataset = 'rajatsurana979/most-streamed-spotify-songs-2023'
    data_path = 'data'
    dataset_file = 'Data-Combined.csv'  # Using the combined dataset for more features

    # Create data directory if it doesn't exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Check if the dataset is already downloaded
    if not os.path.isfile(os.path.join(data_path, dataset_file)):
        # Download the dataset
        api.dataset_download_file(dataset, file_name=dataset_file, path=data_path)
        # Unzip the downloaded file
        import zipfile
        with zipfile.ZipFile(os.path.join(data_path, dataset_file + '.zip'), 'r') as zip_ref:
            zip_ref.extractall(data_path)

    # Read the dataset
    df = pd.read_csv(os.path.join(data_path, dataset_file), encoding='latin1')
    return df

# Load the data
df = load_data()

# Rest of your app code remains the same...
