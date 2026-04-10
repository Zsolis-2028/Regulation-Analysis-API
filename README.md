# Regulation Analysis API

A Dockerized FastAPI backend for analyzing regulation text and extracting structured insights such as summaries, topics, required actions, deadlines, and explanations.

Built as part of my hands-on learning in cloud infrastructure, backend engineering, and AI systems.

---

## 🚀 Features

- Summarize regulation text
- Classify topics
- Extract required actions
- Detect deadlines
- Generate explanations
- Supports multiple analysis modes:
  - Rule-based
  - AI-based
  - Hybrid
- Dockerized for portable deployment

---

## 🧰 Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Docker

---

## 📡 API Endpoints

### Core

- `GET /` → Root check
- `GET /health` → Health check

### Analysis

- `POST /analyze` → Full analysis
- `POST /explain` → AI explanation
- `POST /summarize` → Summary
- `POST /classify` → Extract topics
- `POST /actions` → Required actions
- `POST /deadlines` → Extract deadlines
- `POST /detect` → Rule-based detection

---

## 🧪 Example Request

```json
{
  "text": "The company must submit quarterly reports and train employees annually.",
  "mode": "hybrid"
}
