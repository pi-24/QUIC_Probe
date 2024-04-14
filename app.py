from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
import streamlit as st
import pandas as pd
import streamlit.components.v1 as com
from PIL import Image
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import keyboard
import os
import webbrowser
import base64
import pickle

image_file = 'background.jpg'

with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

st.title('QUIC Probe')
st.write('$$Network$$  $$Traffic$$  $$Classification$$  $$Tool$$')
np.set_printoptions(suppress=True)
# Load the model
with open('finalized_model_lgbm', 'rb') as file:
    model = pickle.load(file)
# Load the labels
class_names = open("labels.txt", "r").readlines()

# Upload the CSV file
uploaded_file = st.file_uploader('Upload a CSV file of your network traffic', type=['csv'])
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.write(df)  # Optionally, display the DataFrame

    # Convert DataFrame to numpy array
    data = df.to_numpy(dtype=np.float32)

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    trafficname = class_name[2:].strip()
    # Display the predicted Traffic Name with Confidence Score
    st.write(f'The Prediction is: $${trafficname}$$')
    st.write(f'Confidence %:', (confidence_score*100).round(3))
    # Useing Webscrap url to open the links
    youtube_url = f"https://www.youtube.com/watch?v=HnDsMehSSY4"
    blog_url = f"https://www.chromium.org/quic/"
    
    
    st.header(f'What QUIC is :')
    col11, col12 = st.columns(2)
    with col11:
        st.write(f'Video')
        if st.button(f'Youtube'):
            webbrowser.open(youtube_url)

    with col12:
        st.write(f'Blog')
        if st.button(f'Blog'):
            webbrowser.open(blog_url)
