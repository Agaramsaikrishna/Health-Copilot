import csv
from eval.scorer import get_score_response , score_response
from agents.copilot_agent import copilot
import os
import csv
import uuid
import pandas as pd
from datetime import datetime



def  get_pre_prompts():
    # Load prompt set
    with open("data/prompts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        prompts = list(reader)
        return prompts
    
def get_eval_runner():
    # Evaluation output
    with open("data/evaluation_results.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "Prompt", "Response", "Expected Keywords", "Expected Tools",
            "Accuracy", "Coherence", "Completeness", "User-Friendliness",
            "Reasoning Used", "Score (0–5)"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        prompts=get_pre_prompts()
        
        for row in prompts:
            query = row["Prompt"]
            expected_keywords = row["Expected Output Keywords"]
            expected_tools = row["Expected Tools"]

            run_response = copilot.run(query)
            response = run_response.content.strip()

            accuracy, coherence, completeness, user_friendly, reasoning_used, score = score_response(
                query, response, expected_keywords, expected_tools
            )

            writer.writerow({
                "Prompt": query,
                "Response": response,
                "Expected Keywords": expected_keywords,
                "Expected Tools": expected_tools,
                "Accuracy": "Yes" if accuracy else "No",
                "Coherence": "Yes" if coherence else "No",
                "Completeness": "Yes" if completeness else "No",
                "User-Friendliness": "Yes" if user_friendly else "No",
                "Reasoning Used": "Yes" if reasoning_used else "No",
                "Score (0–5)": score
            })




def evaluate_prompt(prompt_data):
    """
    Evaluate a single prompt, save results with a unique ID, and return the full evaluation.

    Parameters:
        prompt_data (dict): {
            "prompt": str,
            "expected_keywords": list[str],
            "expected_tools": list[str]
        }

    Returns:
        dict: {
            "id": str,
            "response": str,
            "evaluation": {
                "Accuracy": "Yes"/"No",
                "Coherence": "Yes"/"No",
                "Completeness": "Yes"/"No",
                "User-Friendliness": "Yes"/"No",
                "Reasoning Used": "Yes"/"No",
                "Score (0–5)": float
            }
        }
    """
    os.makedirs("data", exist_ok=True)
    results_file = "data/user_prompt__evaluation_results.csv"

    # Generate unique ID and timestamp
    eval_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat(timespec="seconds")

    # Extract prompt info
    query = prompt_data["prompt"]
    expected_keywords = prompt_data["expected_keywords"]
    expected_tools = prompt_data["expected_tools"]

    print(f"🔍 Evaluating prompt ({eval_id})...")

    # Run the model
    run_response = copilot.run(query)
    response = run_response.content.strip()

    # Score the response
    accuracy, coherence, completeness, user_friendly, reasoning_used, score = get_score_response(
        query, response, expected_keywords, expected_tools
    )

    # Build the result row
    result_row = {
        "ID": eval_id,
        "Timestamp": timestamp,
        "Prompt": query,
        "Response": response,
        "Expected Keywords": ", ".join(expected_keywords),
        "Expected Tools": ", ".join(expected_tools),
        "Accuracy": "Yes" if accuracy else "No",
        "Coherence": "Yes" if coherence else "No",
        "Completeness": "Yes" if completeness else "No",
        "User-Friendliness": "Yes" if user_friendly else "No",
        "Reasoning Used": "Yes" if reasoning_used else "No",
        "Score (0–5)": score
    }

    # Append to CSV
    file_exists = os.path.isfile(results_file)
    with open(results_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(result_row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(result_row)

    print(f"✅ Evaluation complete. Score: {score}\n")

    return {
        "id": eval_id,
        "response": response,
        "evaluation": {
            "Accuracy": result_row["Accuracy"],
            "Coherence": result_row["Coherence"],
            "Completeness": result_row["Completeness"],
            "User-Friendliness": result_row["User-Friendliness"],
            "Reasoning Used": result_row["Reasoning Used"],
            "Score (0–5)": score
        }
    }
