import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train():
    df = pd.read_csv("data/log_samples.csv")
    df.columns = df.columns.str.strip()

    print("Columns:", df.columns.tolist())
    print(df.head())

    X = df["log_text"]
    y = df["label"]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X, y)
    joblib.dump(pipeline, "model/log_classifier.pkl")
    print("Model trained and saved")

if __name__ == "__main__":
    train()