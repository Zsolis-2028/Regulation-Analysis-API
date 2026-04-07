from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .agents.analysis_agent import (
    analyze_regulation,
    analyze_ai,
    analyze_hybrid,
    summarize_text
)

# ---------------------------------------------------------
# RESPONSE MODEL
# ---------------------------------------------------------
class AnalysisResponse(BaseModel):
    input: str
    risk_level: str
    topics: List[str]
    required_actions: List[str]
    deadlines: List[str]
    agencies: List[str]
    notes: List[str]

# ---------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------
app = FastAPI()

# ---------------------------------------------------------
# ANALYZE ENDPOINT
# ---------------------------------------------------------
@app.post("/analyze", response_model=AnalysisResponse)
def analyze(text: str, mode: str = "rule"):
    mode = mode.lower()

    if mode == "rule":
        return analyze_regulation(text)
    elif mode == "ai":
        return analyze_ai(text)
    elif mode == "hybrid":
        return analyze_hybrid(text)
    else:
        return analyze_regulation(text)


# ---------------------------------------------------------
# EXPLAIN ENDPOINT
# ---------------------------------------------------------
@app.post("/explain")
def explain(text: str):
    result = analyze_ai(text)
    narrative_notes = [n for n in result["notes"] if "AI narrative analysis" in n]

    return {
        "input": text,
        "explanation": narrative_notes[0] if narrative_notes else "No narrative generated."
    }


# ---------------------------------------------------------
# SUMMARIZE ENDPOINT
# ---------------------------------------------------------
@app.post("/summarize")
def summarize(text: str):
    return {
        "input": text,
        "summary": summarize_text(text)
    }


# ---------------------------------------------------------
# CLASSIFY ENDPOINT
# ---------------------------------------------------------
@app.post("/classify")
def classify(text: str):
    result = analyze_regulation(text)
    return {
        "input": text,
        "topics": result["topics"]
    }


# ---------------------------------------------------------
# ACTIONS ENDPOINT
# ---------------------------------------------------------
@app.post("/actions")
def actions(text: str):
    result = analyze_regulation(text)
    return {
        "input": text,
        "required_actions": result["required_actions"]
    }


# ---------------------------------------------------------
# DEADLINES ENDPOINT
# ---------------------------------------------------------
@app.post("/deadlines")
def deadlines(text: str):
    result = analyze_regulation(text)
    return {
        "input": text,
        "deadlines": result["deadlines"]
    }


# ---------------------------------------------------------
# DETECT ENDPOINT (full rule-based output)
# ---------------------------------------------------------
@app.post("/detect")
def detect(text: str):
    return analyze_regulation(text)

