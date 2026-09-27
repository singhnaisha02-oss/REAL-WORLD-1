import os

files = {
    ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n.venv/\n*.pkl\n*.pth\n",
    
    "requirements.txt": "fastapi==0.110.0\nuvicorn==0.28.0\nscikit-learn==1.4.1.post1\npandas==2.2.1\nnumpy==1.26.4\nrequests==2.31.0\nstreamlit==1.32.0\n",
    
    "src/__init__.py": "",
    "src/ingestion/__init__.py": "",
    "src/models/__init__.py": "",
    "src/api/__init__.py": "",
    
    "src/ingestion/producer.py": '''import time
import random
import requests

API_URL = "http://localhost:8000/predict"

def generate_user_event():
    is_bot = random.random() < 0.15
    if is_bot:
        return {
            "user_id": f"bot_{random.randint(1, 5)}",
            "ip_entropy": random.uniform(0.1, 0.3),
            "interaction_velocity": random.randint(80, 200),
            "account_age_days": random.randint(0, 3)
        }
    else:
        return {
            "user_id": f"user_{random.randint(100, 999)}",
            "ip_entropy": random.uniform(0.7, 1.0),
            "interaction_velocity": random.randint(1, 15),
            "account_age_days": random.randint(30, 1000)
        }

if __name__ == "__main__":
    print("Starting live event streamer...")
    while True:
        event = generate_user_event()
        try:
            res = requests.post(API_URL, json=event)
            print(f"Sent Event: {event['user_id']} | Response: {res.json()}")
        except Exception:
            print("API not reachable. Ensure FastAPI server is running.")
        time.sleep(0.5)
''',

    "src/models/detector.py": '''import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.15, random_state=42)
        self._fit_dummy_data()

    def _fit_dummy_data(self):
        normal_data = np.random.normal(loc=[0.8, 10, 300], scale=[0.1, 5, 100], size=(500, 3))
        bot_data = np.random.normal(loc=[0.2, 120, 2], scale=[0.05, 20, 1], size=(80, 3))
        X = np.vstack([normal_data, bot_data])
        self.model.fit(X)

    def predict(self, feature_vector: list) -> dict:
        prediction = self.model.predict([feature_vector])[0]
        score = self.model.decision_function([feature_vector])[0]
        return {
            "is_bot": bool(prediction == -1),
            "anomaly_score": round(float(score), 4)
        }
''',

    "src/api/app.py": '''from fastapi import FastAPI
from pydantic import BaseModel
from src.models.detector import AnomalyDetector

app = FastAPI(title="Real-Time Botnet Detection API")
detector = AnomalyDetector()

class EventPayload(BaseModel):
    user_id: str
    ip_entropy: float
    interaction_velocity: int
    account_age_days: int

@app.post("/predict")
def predict_event(payload: EventPayload):
    features = [payload.ip_entropy, payload.interaction_velocity, payload.account_age_days]
    result = detector.predict(features)
    return {
        "user_id": payload.user_id,
        "is_bot": result["is_bot"],
        "anomaly_score": result["anomaly_score"],
        "status": "FLAGGED" if result["is_bot"] else "CLEARED"
    }
''',

    "dashboard/app.py": '''import streamlit as st
import requests

st.title("Real-Time Fraud & Botnet Detection Center")

st.markdown("### Test Individual Stream Event")
ip_entropy = st.slider("IP Entropy (Low = Suspicious)", 0.0, 1.0, 0.8)
velocity = st.slider("Interaction Velocity (Clicks/min)", 1, 200, 10)
account_age = st.number_input("Account Age (Days)", min_value=0, value=100)

if st.button("Evaluate Event"):
    payload = {
        "user_id": "test_user_1",
        "ip_entropy": ip_entropy,
        "interaction_velocity": velocity,
        "account_age_days": account_age
    }
    try:
        response = requests.post("http://localhost:8000/predict", json=payload).json()
        if response["is_bot"]:
            st.error(f"ALERT: Potential Bot Activity Detected! Score: {response['anomaly_score']}")
        else:
            st.success(f"Transaction Cleared. Score: {response['anomaly_score']}")
    except Exception:
        st.warning("Ensure FastAPI server is running on localhost:8000")
''',

    "README.md": '''# Real-Time Botnet & Engagement Fraud Detection System

An end-to-end Machine Learning pipeline designed to detect coordinated bot activity and fake engagement in real-time streams using Isolation Forests and REST APIs.

## Tech Stack
- **API Engine:** FastAPI, Uvicorn
- **ML Framework:** Scikit-Learn
- **Dashboard:** Streamlit

## Quickstart
1. `pip install -r requirements.txt`
2. `uvicorn src.api.app:app --reload --port 8000`
3. `streamlit run dashboard/app.py`
4. `python -m src.ingestion.producer`
'''
}

# Create base directory
base_dir = "realtime-botnet-detector"
os.makedirs(base_dir, exist_ok=True)

# Generate files and directories
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Project directory successfully generated in '{base_dir}'!")
