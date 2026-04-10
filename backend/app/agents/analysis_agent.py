def analyze_regulation(text: str):
    return {
        "input": text,
        "risk_level": "medium",
        "topics": ["compliance", "reporting"],
        "required_actions": ["submit report", "train employees"],
        "deadlines": ["30 days"],
        "agencies": ["regulatory body"],
        "notes": ["Rule-based analysis"]
    }


def analyze_ai(text: str):
    return {
        "input": text,
        "risk_level": "low",
        "topics": ["AI analysis"],
        "required_actions": ["review compliance"],
        "deadlines": ["quarterly"],
        "agencies": ["internal"],
        "notes": ["AI narrative analysis"]
    }


def analyze_hybrid(text: str):
    rule = analyze_regulation(text)
    ai = analyze_ai(text)

    return {
        "input": text,
        "risk_level": "medium",
        "topics": list(set(rule["topics"] + ai["topics"])),
        "required_actions": list(set(rule["required_actions"] + ai["required_actions"])),
        "deadlines": list(set(rule["deadlines"] + ai["deadlines"])),
        "agencies": list(set(rule["agencies"] + ai["agencies"])),
        "notes": ["Hybrid analysis"]
    }


def summarize_text(text: str):
    return text[:100] + "..." if len(text) > 100 else text