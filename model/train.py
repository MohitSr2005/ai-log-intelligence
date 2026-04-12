from pathlib import Path
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "log_samples.csv"
MODEL_PATH = BASE_DIR / "model" / "log_classifier.pkl"


def train_model() -> None:
    df = pd.read_csv(DATA_PATH)

    required_columns = {"log_text", "label"}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV must contain 'log_text' and 'label' columns.")

    df = df.dropna(subset=["log_text", "label"])

    X = df["log_text"].astype(str)
    y = df["label"].astype(str)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("clf", MultinomialNB())
    ])

    pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"Model trained successfully on {len(df)} samples")
    print(f"Saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()