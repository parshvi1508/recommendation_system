import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model_utils import detect_anomalies

st.title("📊 E-Learning Anomaly Detection Dashboard")
uploaded_file = st.file_uploader("Upload learner activity CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    anomalies = detect_anomalies(df)
    st.subheader("📌 Anomalies")
    st.dataframe(anomalies)
    st.subheader("📉 Scatter Plot")
    sns.scatterplot(x='num_course_views', y='quiz_accuracy', data=df, hue='anomaly_score')
    st.pyplot(plt.gcf())