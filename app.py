import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model_utils import detect_anomalies, train_model
import os
from twilio.rest import Client 

st.set_page_config(page_title="E-Learning Anomaly Detection", layout="wide")
st.title("📊 E-Learning Anomaly Detection Dashboard")

uploaded_file = st.file_uploader("Upload Student Data CSV", type="csv")

st.sidebar.subheader("📱 Notification Settings")
twilio_enabled = st.sidebar.checkbox("Enable SMS Notifications")
if twilio_enabled:
    account_sid = st.sidebar.text_input("Twilio Account SID", type="password")
    auth_token = st.sidebar.text_input("Twilio Auth Token", type="password")
    from_number = st.sidebar.text_input("Twilio Phone Number")
    to_number = st.sidebar.text_input("Your Phone Number")

if uploaded_file:
    with st.spinner('Processing data...'):
        # Read the data
        df = pd.read_csv(uploaded_file, encoding='latin-1')
        
        # First train the model
        st.info('Training model...')
        trained_df = train_model(df)
        
        # Then detect anomalies
        st.info('Detecting anomalies...')
        anomalies = detect_anomalies(df)
        if twilio_enabled and len(anomalies) > 0:
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Alert: Found {len(anomalies)} students with unusual learning patterns.",
                    from_=from_number,
                    to=to_number
                )
                st.sidebar.success("SMS notification sent!")
            except Exception as e:
                st.sidebar.error(f"Failed to send SMS: {str(e)}")

        # Show results
        st.success(f"Found {len(anomalies)} potential anomalies")
        
        # Display anomalies
        st.subheader("📌 Anomalies Detected")
        st.dataframe(anomalies)
        
        # Visualization
        st.subheader("📉 Engagement Pattern Analysis")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, 
                       x='video_completion_rate', 
                       y='quiz_accuracy',
                       hue='anomaly_score',
                       palette=['red', 'blue'])
        plt.title("Video Completion vs Quiz Performance")
        st.pyplot(fig)