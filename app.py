import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model_utils import detect_anomalies, train_model
import os
from twilio.rest import Client 
import plotly.express as px 
import joblib

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
        
        # ======== NEW CODE STARTS HERE (INSIDE THE UPLOADED_FILE BLOCK) ========
        st.sidebar.subheader("🔍 Filter Anomaly Types")
        anomaly_types = {
            'High Video Time + Low Scores': (df['avg_time_per_video'] > 40) & (df['quiz_accuracy'] < 50),
            'Low Forum Activity': df['forum_activity'] == 0,
            'Video Binging (High Completion + Low Quiz)': (df['video_completion_rate'] > 80) & (df['quiz_accuracy'] < 40),
            'Location Hopper': df['location_change'] > 5
        }
        
        selected_anomalies = st.sidebar.multiselect(
            'Select anomaly types to highlight:',
            options=list(anomaly_types.keys())
        )

        plot_df = df.copy()
        plot_df['highlight'] = False
        for anomaly_type in selected_anomalies:
            plot_df.loc[anomaly_types[anomaly_type], 'highlight'] = True

        # Add interactive plot
        st.subheader("👤 Student Profile Explorer")
        filtered_students = plot_df[plot_df['highlight']]['student_id'].tolist()
        selected_student = st.selectbox("Or select a student:", options=filtered_students)

        if selected_student:
            student_data = df[df['student_id'] == selected_student].iloc[0]
            
            with st.expander(f"📚 Full Profile: {selected_student}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Avg Time/Video", f"{student_data['avg_time_per_video']:.1f} mins")
                    st.metric("Forum Posts", student_data['forum_activity'])
                    st.metric("Location Changes", student_data['location_change'])
                    
                with col2:
                    st.metric("Video Completion", f"{student_data['video_completion_rate']}%")
                    st.metric("Quiz Accuracy", f"{student_data['quiz_accuracy']}%")
                    st.metric("Course Views", student_data['num_course_views'])
                    
            if st.button("📩 Generate Personalized Recommendation"):
                if student_data['quiz_accuracy'] < 40 and student_data['video_completion_rate'] > 70:
                    st.success("Recommendation: Found video binging without comprehension → Assign 'Active Learning Strategies' module")
                elif student_data['forum_activity'] == 0:
                    st.success("Recommendation: Isolated learner → Connect with study group #3")

        # Add tabs for different views
        tab1, tab2, tab3 = st.tabs(["Engagement Trends", "Time Analysis", "Location Patterns"])

        with tab1:
            fig = px.histogram(df, x='num_course_views', nbins=20, title="Course View Distribution")
            st.plotly_chart(fig)

        with tab2:
            fig = px.box(df, y='avg_time_per_video', points="all", hover_data=['student_id'])
            st.plotly_chart(fig)

        with tab3:
            fig = px.pie(df, names='location_change', title="Device Switching Behavior")
            st.plotly_chart(fig)
