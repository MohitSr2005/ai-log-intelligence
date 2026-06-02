import pandas as pd
from model.predict import classify_log

# Load test dataset
df = pd.read_csv("data/test_logs.csv")

correct = 0
total = len(df)

print("\n=== MODEL EVALUATION ===\n")

for _, row in df.iterrows():
    log_text = row["log_text"]
    expected = row["expected_issue"]

    prediction = classify_log(log_text)
    predicted = prediction["issue_type"]

    print(f"Log: {log_text}")
    print(f"Expected: {expected}")
    print(f"Predicted: {predicted}")
    print("-" * 50)

    if predicted == expected:
        correct += 1

accuracy = (correct / total) * 100

print(f"\nAccuracy: {accuracy:.2f}%")
print(f"Correct: {correct}/{total}")