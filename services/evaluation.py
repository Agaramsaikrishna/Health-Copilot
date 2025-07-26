import json
from datetime import datetime

EVAL_FILE = "evaluations/eval_results.json"

def evaluate_response(response_text: str, scores: dict, notes: str = ""):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "response": response_text,
        "scores": scores,
        "average_score": round(sum(scores.values()) / len(scores), 2),
        "notes": notes
    }

    try:
        with open(EVAL_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(EVAL_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return entry
