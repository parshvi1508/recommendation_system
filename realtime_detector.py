import pandas as pd
from model_utils import detect_anomalies, FEATURE_COLS
from alerts import send_email_alert, send_sms_alert

def main():
    df = pd.read_csv("data_stream.csv")
    anomalies = detect_anomalies(df)
    for _, row in anomalies.iterrows():
        msg = f"Anomaly detected: User {row['user_id']} - {row[FEATURE_COLS].to_dict()}"
        print(msg)
        send_email_alert("Anomaly Detected", msg)
        send_sms_alert(msg)

if __name__ == "__main__":
    main()