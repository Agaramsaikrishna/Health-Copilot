import requests
from agno.tools import tool


@tool(name="get_openfoodfacts_nutrition", description="Retrieve nutrition info for packaged foods using OpenFoodFacts")
def get_openfoodfacts_nutrition(product_name: str) -> str:
    """
    Fetches basic nutritional data from OpenFoodFacts for a given food product.

    Args:
        product_name (str): Product name or keyword (e.g., "oats", "banana")

    Returns:
        str: Nutrition summary like kcal per 100g.

    Notes:
        This API does not require authentication.
        Documentation: https://world.openfoodfacts.org/data
    """
    res = requests.get(
        f"https://world.openfoodfacts.org/cgi/search.pl",
        params={"search_terms": product_name, "search_simple": 1, "json": 1}
    )
    products = res.json().get("products", [])
    if not products:
        return "Food item not found."
    item = products[0]
    return f"{item.get('product_name', 'Unknown')} - {item.get('nutriments', {}).get('energy-kcal_100g', '?')} kcal per 100g"



@tool(name="search_nutritionix_food", description="Get nutrition info (calories, protein) for specific food items.")
def search_nutritionix_food(query: str) -> dict:
    """
    Search calories and protein for a specific food using the Nutritionix API.

    Args:
        query (str): A clear, simple food description like "1 cup rice", "banana", or "grilled chicken".
                     Avoid broad health goals (e.g., "healthy food for diabetes").

    Returns:
        dict: A dictionary containing nutrition facts like calories, protein, carbs, fat, etc.
              Returns an error message if no match is found.

    Example:
        search_nutritionix_food("2 boiled eggs")

    Notes:
        - Requires a valid Nutritionix API key (x-app-id and x-app-key).
        - Nutritionix does not support vague or medical queries. Use actual food names only.
    """
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": "272aaf64",
        "x-app-key": "fe3e213727ebb2340df59d81707783d1",
        "Content-Type": "application/json",
    }
    data = {"query": query}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()
        foods = res_json.get("foods", [])

        if not foods:
            return {"error": "No food found. Use simple queries like '1 cup rice' or 'grilled chicken'."}

        item = foods[0]
        return {
            'food_name': item.get('food_name'),
            'brand_name': item.get('brand_name'),
            'serving_qty': item.get('serving_qty'),
            'serving_unit': item.get('serving_unit'),
            'serving_weight_grams': item.get('serving_weight_grams'),
            'nf_calories': item.get('nf_calories'),
            'nf_total_fat': item.get('nf_total_fat'),
            'nf_saturated_fat': item.get('nf_saturated_fat'),
            'nf_cholesterol': item.get('nf_cholesterol'),
            'nf_sodium': item.get('nf_sodium'),
            'nf_total_carbohydrate': item.get('nf_total_carbohydrate'),
            'nf_dietary_fiber': item.get('nf_dietary_fiber'),
            'nf_sugars': item.get('nf_sugars'),
            'nf_protein': item.get('nf_protein'),
            'nf_potassium': item.get('nf_potassium'),
            'nf_p': item.get('nf_p')
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}