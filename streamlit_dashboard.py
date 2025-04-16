import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model_utils import detect_anomalies, train_model
import os 
st.set_page_config(page_title="E-Learning Anomaly Detection", layout="wide")
st.title("📊 E-Learning Anomaly Detection Dashboard")

'''
uploaded_file = st.file_uploader("Upload learner activity CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='latin-1')
    anomalies = detect_anomalies(df)
    st.subheader("📌 Anomalies")
    st.dataframe(anomalies)
    st.subheader("📉 Scatter Plot")
    sns.scatterplot(x='num_course_views', y='quiz_accuracy', data=df, hue='anomaly_score')
    st.pyplot(plt.gcf())
    '''
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Train Model")
    train_file = st.file_uploader("Upload training data CSV", type="csv", key="train")
    if train_file:
        train_df = pd.read_csv(train_file, encoding='latin-1')
        if st.button("Train Model"):
            with st.spinner('Training model...'):
                train_model(train_df)
                st.success("✅ Model trained successfully!")

with col2:
    st.subheader("2. Detect Anomalies")
    predict_file = st.file_uploader("Upload data to analyze", type="csv", key="predict")
    
    if predict_file:
        if not (os.path.exists("anomaly_model.pkl") and os.path.exists("scaler.pkl")):
            st.error("⚠️ Please train the model first!")
        else:
            df = pd.read_csv(predict_file, encoding='latin-1')
            anomalies = detect_anomalies(df)
            st.write("Found", len(anomalies), "anomalies")
            st.dataframe(anomalies)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(x='num_course_views', y='quiz_accuracy', 
                          data=df, hue='anomaly_score')
            plt.title("Anomaly Detection Results")
            st.pyplot(fig)