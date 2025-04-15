from model_utils import generate_sample_data, train_model

if __name__ == "__main__":
    df = generate_sample_data()
    df = train_model(df)
    print("Model trained. Sample anomalies:")
    print(df[df['anomaly_score'] == -1])