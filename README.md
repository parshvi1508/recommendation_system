# E-Learning Anomaly Detection System

## 📦 Features
- Detects unusual learner activity using Isolation Forest.
- Real-time alerts via email/SMS (optional).
- Interactive Streamlit dashboard.
- Docker-ready deployment.

## 🚀 Quick Start

### Option 1: Run Everything with One Command
```bash
python run_all.py
```

### Option 2: Docker
```bash
docker-compose up --build
```

Then open [http://localhost:8501](http://localhost:8501).

## 🔍 Data Columns
- avg_time_per_video (min)
- num_course_views
- num_recommend_clicks
- quiz_accuracy (%)
- forum_activity
- location_change (0 or 1)

## ✅ Customize Alerts
Edit `.env` or update docker-compose.yml with your Gmail or Twilio credentials.