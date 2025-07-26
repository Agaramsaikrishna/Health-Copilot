def score_response(prompt, response, expected_keywords, expected_tools):
    """
    Evaluate an LLM response with qualitative and quantitative metrics.

    Returns:
        accuracy (bool), coherence (bool), completeness (bool),
        user_friendly (bool), reasoning_used (bool), score (float)
    """
    # Normalize text
    response = response.lower()
    expected_keywords = expected_keywords.lower().split(",")
    expected_tools = expected_tools.lower().split(",")

    # Quantitative
    accuracy = all(keyword.strip() in response for keyword in expected_keywords)
    tools_triggered = all(tool.strip() in response for tool in expected_tools)

    # Qualitative (simple heuristics — can improve with NLP techniques or LLM evals)
    coherence = response.endswith(".") and len(response.split()) > 10
    completeness = len(expected_keywords) <= len([kw for kw in expected_keywords if kw.strip() in response])
    user_friendly = not any(word in response for word in ["error", "unavailable", "undefined"])

    # Reasoning (detect planning or multi-step patterns)
    reasoning_used = any(phrase in response for phrase in ["step 1", "plan:", "first,", "next,", "finally"])

    # Weighted scoring system (0–5)
    score = (
        1.0 * accuracy +
        1.0 * tools_triggered +
        1.0 * coherence +
        1.0 * completeness +
        1.0 * user_friendly
    )
    score = round(score, 2)

    return accuracy, coherence, completeness, user_friendly, reasoning_used, score




def get_score_response(prompt, response, expected_keywords, expected_tools):
    """
    Evaluate an LLM response with qualitative and quantitative metrics.
    
    Returns:
        accuracy (bool), coherence (bool), completeness (bool),
        user_friendly (bool), reasoning_used (bool), score (float)
    """
    response = response.lower()
    expected_keywords = expected_keywords.lower().split(",") if expected_keywords else []
    expected_tools = expected_tools.lower().split(",") if expected_tools else []

    # 🔎 Accuracy: did response include all expected keywords?
    accuracy = all(keyword.strip() in response for keyword in expected_keywords if keyword.strip())

    # 🛠️ Tool usage: simulate by checking for tool names
    tools_triggered = all(tool.strip() in response for tool in expected_tools if tool.strip())

    # 🧠 Reasoning: basic check for chain-of-thought or structured thinking
    reasoning_used = any(phrase in response for phrase in [
        "step 1", "step 2", "plan:", "analyze", "next,", "solve:", "then,", "finally"
    ])

    # 🧩 Coherence: basic grammar/length check
    coherence = response.endswith(".") and len(response.split()) > 15

    # ✅ Completeness: includes at least as many keywords as expected
    completeness = len(expected_keywords) <= sum(keyword.strip() in response for keyword in expected_keywords)

    # 🙋 User-friendly: avoids technical errors or vague failure
    user_friendly = not any(word in response for word in ["error", "undefined", "null", "n/a"])

    # 📊 Weighted scoring (0–5)
    score = (
        1.0 * accuracy +
        1.0 * tools_triggered +
        1.0 * coherence +
        1.0 * completeness +
        1.0 * user_friendly
    )
    score = round(score, 2)

    return accuracy, coherence, completeness, user_friendly, reasoning_used, score

