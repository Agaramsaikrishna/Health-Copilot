from agno.tools import tool

@tool(name="get_diet_tip", description="Get a practical diet tip based on a specific health or nutrition goal.")
def get_diet_tip(goal: str = "weight loss") -> str:
    """
    Provide a practical diet tip based on a user's specific health or lifestyle goal.

    Parameters:
    ----------
    goal : str
        The user's dietary or health-related goal. Supported values include:
        - "weight loss"
        - "muscle gain"
        - "general health"
        - "heart health"
        - "diabetes management"
        - "gut health"
        - "energy boost"
        - "mental focus"

    Returns:
    -------
    str
        A simple, actionable diet tip tailored to the specified goal. If the goal is unknown,
        a general health tip will be provided.
    """

    tips = {
        "weight loss": (
            "Focus on portion control, eat more fiber-rich foods like oats, lentils, and vegetables, "
            "and avoid sugary drinks. Aim for a slight calorie deficit and increase your daily movement."
        ),
        "muscle gain": (
            "Consume enough protein throughout the day (e.g., chicken, eggs, tofu, legumes), "
            "eat calorie-dense whole foods, and ensure you're training consistently with resistance exercises."
        ),
        "general health": (
            "Eat a balanced diet with a variety of whole foods, stay hydrated, move daily, get enough sleep, "
            "and manage stress effectively."
        ),
        "heart health": (
            "Prioritize foods rich in omega-3 fatty acids like salmon and flaxseeds, reduce sodium intake, "
            "limit processed foods, and maintain a healthy weight through regular activity."
        ),
        "diabetes management": (
            "Choose complex carbohydrates (e.g., whole grains, legumes), avoid refined sugars, monitor portion sizes, "
            "and eat meals consistently throughout the day to maintain blood sugar levels."
        ),
        "gut health": (
            "Include fermented foods like yogurt and kefir, eat high-fiber fruits and vegetables, stay hydrated, "
            "and limit processed food and artificial sweeteners."
        ),
        "energy boost": (
            "Eat small, balanced meals throughout the day with complex carbs, healthy fats, and lean proteins. "
            "Avoid excess caffeine and stay hydrated."
        ),
        "mental focus": (
            "Fuel your brain with omega-3 fats, whole grains, leafy greens, and adequate hydration. "
            "Limit added sugar and get enough sleep."
        ),
    }

    return tips.get(goal.lower(), "Eat healthy, stay active, and tailor your nutrition to your personal needs and goals.")
