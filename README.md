# REAL-WORLD-1
# Real-Time Botnet & Fake Engagement Detection Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end Machine Learning pipeline designed to detect coordinated botnet attacks, fake interactions, and engagement fraud in low-latency event streams. Built to mirror production fraud-detection systems at scale.

---

## Key Features

- **Low-Latency Anomaly Detection:** Uses an Unsupervised Isolation Forest model to flag high-velocity, low-entropy interaction clusters.
- **RESTful API Serving:** Exposes a sub-100ms inference endpoint via FastAPI for real-time scoring.
- **Interactive Monitoring Dashboard:** Built with Streamlit to visualize flagged user events and test arbitrary feature payloads.
- **Synthetic Stream Producer:** Simulates concurrent normal user behavior vs. synchronized bot activity.

---

## System Architecture

```text
[ Live Event Stream ] ──> [ FastAPI Inference Endpoint ] ──> [ Isolation Forest Model ]
                                    │                                  │
                                    ▼                                  ▼
                        [ Streamlit Dashboard ] <─── [ Score / Fraud Flag Result ]
