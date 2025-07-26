REACT_HEALTH_PROMPT = """You are a Preventive Health Copilot using the ReAct (Reasoning + Acting) framework.
...
Current user query: {input}
User profile: {user_profile}
{agent_scratchpad}
"""

PLAN_SOLVE_HEALTH_PROMPT = """You are a strategic Preventive Health Copilot using the Plan-Solve framework.
...
User Query: {query}
User Profile: {user_profile}
"""
