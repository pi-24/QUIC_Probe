import streamlit as st
import pandas as pd
from collections import Counter
import joblib
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

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

# Load the saved model
loaded_model = joblib.load('traffic_classifier.pkl')

def predict_traffic(test_data):
    if test_data.empty:
        return {}
    X_test = test_data[['relativetime', 'packetsize', 'packetdirection']]
    predictions = loaded_model.predict(X_test)
    total_predictions = len(predictions)
    class_counts = Counter(predictions)
    class_accuracy_rates = {class_name: count / total_predictions for class_name, count in class_counts.items()}
    return class_accuracy_rates

def plot_accuracy_rates(accuracy_rates):
    classes = ['Google Search', 'Google Drive', 'Google Music', 'YouTube', 'Google Docs']
    rates = [accuracy_rates.get(i, 0) for i in range(5)]
    fig, ax = plt.subplots()
    ax.bar(classes, rates, color='skyblue')
    ax.set_ylabel('Accuracy Rate')
    ax.set_xlabel('Traffic Type')
    ax.set_title('Prediction Accuracy Rates')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def main():
    st.title('AI-Powered QUIC Traffic Classifier')
    st.write("### Enhancing Cybersecurity Through AI-Driven QUIC Traffic Classification")
    
    st.markdown("""
    **Project Overview:**
    - This tool classifies QUIC traffic, overcoming the challenge of encryption at the transport layer.
    - Uses **LightGBM (Light Gradient Boosting Machine)** for accurate classification.
    - Features analyzed: **Packet Size, Timestamp, Relative Time, Packet Direction**.
    - Helps cybersecurity teams and ISPs monitor QUIC traffic while preserving privacy.
    """)
    
    st.sidebar.title('File Selection')
    test_cases = ['GoogleDoc-3.txt', 'GoogleDrive-test1.txt', 'GoogleMusic-8.txt', 'GoogleSearch-7.txt', 'Youtube-20.txt']
    selected_option = st.sidebar.radio('Select a file or upload your own', ('Choose a test file', 'Upload a file'))
    
    if selected_option == 'Choose a test file':
        selected_file = st.sidebar.selectbox('Select a test file', test_cases)
        test_data = pd.read_csv(selected_file, header=None, sep='\t', names=['timestamp', 'relativetime', 'packetsize', 'packetdirection'])
        st.subheader("Data Sample:")
        st.dataframe(test_data.head())
    else:
        uploaded_file = st.sidebar.file_uploader('Upload a .txt file', type='txt')
        if uploaded_file is not None:
            content = uploaded_file.getvalue()
            file_obj = io.StringIO(content.decode('utf-8'))
            test_data = pd.read_csv(file_obj, header=None, sep='\t', names=['timestamp', 'relativetime', 'packetsize', 'packetdirection'])
            st.subheader("Data Sample:")
            st.dataframe(test_data.head())
    
    if st.button('Run Prediction'):
        accuracy_rates = predict_traffic(test_data)
        st.write('### Prediction Accuracy Rates:')
        max_accuracy = max(accuracy_rates.values())
        for class_no, accuracy_rate in accuracy_rates.items():
            class_name = ['Google Search', 'Google Drive', 'Google Music', 'YouTube', 'Google Docs'][class_no]
            color = '#009900' if accuracy_rate == max_accuracy else '#990000'
            st.markdown(f'<span style="background-color:{color}; padding: 5px; border-radius: 5px;">{class_name}: {accuracy_rate:.2f}</span>', unsafe_allow_html=True)
        plot_accuracy_rates(accuracy_rates)

if __name__ == '__main__':
    main()
