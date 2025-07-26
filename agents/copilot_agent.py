from agno.agent import Agent, RunResponse
from agno.models.together import Together
from agno.models.groq import Groq
from agno.tools.wikipedia import WikipediaTools
from utils.instructions import FIRST_instruction
from dotenv import load_dotenv
import os 
import json
from keys import *
from tools.health_risk import health_risk_assessment
from services.exercise import get_exercise_plan
from services.reminder import schedule_reminder
from services.evaluation import evaluate_response
from tools.nutrition_api import get_openfoodfacts_nutrition , search_nutritionix_food
from typing import Dict, List, Optional, Any






copilot = Agent(
    model=Together(id=REASONING_MODEL , api_key=TOGETHER_API_KEY),
    tools=[ health_risk_assessment, schedule_reminder , search_nutritionix_food , get_openfoodfacts_nutrition, get_exercise_plan ,WikipediaTools()],
    description="You are a Preventive Health Copilot. Use the tool to assess user health profile and recommend screenings.",
    show_tool_calls=True,
    reasoning=True,
    instructions=FIRST_instruction,
    
)






