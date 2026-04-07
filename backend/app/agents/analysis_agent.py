import re

# ---------------------------------------------------------
# RULE-BASED ENGINE
# ---------------------------------------------------------
def analyze_regulation(text: str):
    text_lower = text.lower()

    # 1. Risk detection
    risk_keywords = ["penalty", "penalties", "fine", "audit", "violation", "non-compliance"]
    severity_score = sum(2 for word in risk_keywords if word in text_lower)

    if severity_score >= 4:
        risk_level = "Critical"
    elif severity_score == 2:
        risk_level = "High"
    else:
        risk_level = "Low"

    # 2. Topic classification
    topics = []
    if "data" in text_lower or "personal" in text_lower:
        topics.append("Data Protection")
    if "encrypt" in text_lower or "security" in text_lower:
        topics.append("Security Requirements")
    if "employee" in text_lower:
        topics.append("Employee Obligations")
    if "report" in text_lower or "notify" in text_lower:
        topics.append("Reporting Requirements")
    if "prohibit" in text_lower or "must not" in text_lower or "may not" in text_lower:
        topics.append("Prohibited Actions")

    # 3. Required actions
    required_actions = []
    if "encrypt" in text_lower:
        required_actions.append("Ensure encryption of personal data")
    if "report" in text_lower or "notify" in text_lower:
        required_actions.append("Prepare reporting or notification workflow")
    if "audit" in text_lower:
        required_actions.append("Prepare for compliance audits")
    if "must not" in text_lower or "may not" in text_lower:
        required_actions.append("Identify and restrict prohibited actions")

    # 4. Deadlines
    deadlines = []
    deadline_patterns = [
        r"within \d+ days",
        r"no later than \d+ days",
        r"immediately",
        r"annually",
        r"quarterly",
        r"by \w+ \d{1,2}, \d{4}"
    ]
    for pattern in deadline_patterns:
        deadlines.extend(re.findall(pattern, text_lower))

    # 5. Agencies
    agencies = []
    agency_keywords = {
        "ftc": "Federal Trade Commission",
        "osha": "Occupational Safety and Health Administration",
        "sec": "Securities and Exchange Commission",
        "hipaa": "HIPAA Compliance Authority",
        "gdpr": "GDPR Supervisory Authority"
    }
    for key, name in agency_keywords.items():
        if key in text_lower:
            agencies.append(name)

    # 6. Notes
    notes = []
    if "non-compliance" in text_lower:
        notes.append("Non-compliance triggers penalties or audits")
    if deadlines:
        notes.append(f"Detected deadlines: {deadlines}")
    if agencies:
        notes.append(f"Relevant enforcement agencies: {agencies}")

    return {
        "input": text,
        "risk_level": risk_level,
        "topics": topics,
        "required_actions": required_actions,
        "deadlines": deadlines,
        "agencies": agencies,
        "notes": notes
    }


# ---------------------------------------------------------
# AI ENGINE (adds narrative)
# ---------------------------------------------------------
def analyze_ai(text: str):
    base = analyze_regulation(text)

    risk = base.get("risk_level", "Unknown")
    topics = base.get("topics", [])
    actions = base.get("required_actions", [])
    deadlines = base.get("deadlines", [])
    agencies = base.get("agencies", [])

    narrative_parts = [
        f"This text appears to present a {risk.lower()} level of regulatory or compliance risk."
    ]

    if topics:
        narrative_parts.append(f"It relates to: {', '.join(topics)}.")
    if actions:
        narrative_parts.append("Required actions include: " + "; ".join(actions) + ".")
    if deadlines:
        narrative_parts.append("Detected deadlines: " + "; ".join(deadlines) + ".")
    if agencies:
        narrative_parts.append("Relevant agencies: " + ", ".join(agencies) + ".")

    narrative = " ".join(narrative_parts)
    base["notes"].append(f"AI narrative analysis: {narrative}")

    return base


# ---------------------------------------------------------
# HYBRID MERGE MODE (strongest)
# ---------------------------------------------------------
def analyze_hybrid(text: str):
    rule = analyze_regulation(text)
    ai = analyze_ai(text)

    # 1. Highest severity wins
    severity_order = {"Low": 1, "High": 2, "Critical": 3}
    rule_risk = rule.get("risk_level", "Low")
    ai_risk = ai.get("risk_level", "Low")
    final_risk = rule_risk if severity_order[rule_risk] >= severity_order[ai_risk] else ai_risk

    # 2. Merge lists (dedupe)
    def merge_lists(a, b):
        return list(dict.fromkeys(a + b))

    final_topics = merge_lists(rule["topics"], ai["topics"])
    final_actions = merge_lists(rule["required_actions"], ai["required_actions"])
    final_deadlines = merge_lists(rule["deadlines"], ai["deadlines"])
    final_agencies = merge_lists(rule["agencies"], ai["agencies"])
    final_notes = merge_lists(rule["notes"], ai["notes"])

    return {
        "input": text,
        "risk_level": final_risk,
        "topics": final_topics,
        "required_actions": final_actions,
        "deadlines": final_deadlines,
        "agencies": final_agencies,
        "notes": final_notes
    }


# ---------------------------------------------------------
# SUMMARY ENGINE
# ---------------------------------------------------------
def summarize_text(text: str):
    sentences = re.split(r'[.!?]', text)
    summary = sentences[0].strip()

    if len(summary) < 10:
        summary = text[:120] + "..."

    return summary

