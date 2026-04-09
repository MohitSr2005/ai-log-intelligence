import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.analyzer import analyze_log

test_logs = [
    "Database connection refused on port 5432",
    "JWT token expired for user request",
    "504 Gateway Timeout from nginx server",
    "ModuleNotFoundError: No module named numpy",
    "Environment variable SECRET_KEY missing",
    "500 Internal Server Error at /login endpoint"
]

for log in test_logs:
    result = analyze_log(log)
    print("\nLOG:", log)
    print("OUTPUT:", result)