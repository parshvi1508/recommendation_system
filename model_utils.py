import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

MODEL_PATH = "anomaly_model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURE_COLS = [
    'avg_time_per_video',
    'num_course_views',
    'num_recommend_clicks',
    'quiz_accuracy',
    'forum_activity',
    'location_change'
]

def generate_sample_data():
    np.random.seed(42)
    return pd.DataFrame({
        'user_id': np.arange(1, 101),
        'avg_time_per_video': np.random.uniform(2, 60, 100),
        'num_course_views': np.random.randint(10, 100, 100),
        'num_recommend_clicks': np.random.randint(0, 30, 100),
        'quiz_accuracy': np.random.uniform(0, 100, 100),
        'forum_activity': np.random.randint(0, 50, 100),
        'location_change': np.random.choice([0, 1], size=100),
    })

def train_model(df):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[FEATURE_COLS])
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    df['anomaly_score'] = model.fit_predict(X_scaled)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    return df

def detect_anomalies(df):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    X_scaled = scaler.transform(df[FEATURE_COLS])
    df['anomaly_score'] = model.predict(X_scaled)
    return df[df['anomaly_score'] == -1]