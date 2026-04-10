from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.agents.analysis_agent import (
    analyze_regulation,
    analyze_ai,
    analyze_hybrid,
    summarize_text
)

app = FastAPI()

# -------------------------
# Request Model
# -------------------------
class TextRequest(BaseModel):
    text: str
    mode: str = "rule"

# -------------------------
# Root
# -------------------------
@app.get("/")
def read_root():
    return {"message": "FastAPI is working"}

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Analyze
# -------------------------
@app.post("/analyze")
def analyze(req: TextRequest):
    mode = req.mode.lower()

    if mode == "rule":
        return analyze_regulation(req.text)
    elif mode == "ai":
        return analyze_ai(req.text)
    elif mode == "hybrid":
        return analyze_hybrid(req.text)
    else:
        return analyze_regulation(req.text)

# -------------------------
# Explain
# -------------------------
@app.post("/explain")
def explain(req: TextRequest):
    result = analyze_ai(req.text)
    return {
        "input": req.text,
        "explanation": result["notes"][0]
    }

# -------------------------
# Summarize
# -------------------------
@app.post("/summarize")
def summarize(req: TextRequest):
    return {
        "input": req.text,
        "summary": summarize_text(req.text)
    }

# -------------------------
# Classify
# -------------------------
@app.post("/classify")
def classify(req: TextRequest):
    result = analyze_regulation(req.text)
    return {
        "input": req.text,
        "topics": result["topics"]
    }

# -------------------------
# Actions
# -------------------------
@app.post("/actions")
def actions(req: TextRequest):
    result = analyze_regulation(req.text)
    return {
        "input": req.text,
        "required_actions": result["required_actions"]
    }

# -------------------------
# Deadlines
# -------------------------
@app.post("/deadlines")
def deadlines(req: TextRequest):
    result = analyze_regulation(req.text)
    return {
        "input": req.text,
        "deadlines": result["deadlines"]
    }

# -------------------------
# Detect
# -------------------------
@app.post("/detect")
def detect(req: TextRequest):
    return analyze_regulation(req.text)