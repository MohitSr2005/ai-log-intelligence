from pathlib import Path
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("\n=== TRAINING EVALUATION ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print(classification_report(y_test, y_pred))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"Model trained successfully on {len(df)} samples")
    print(f"Saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()