# 🩺 Preventive Health Copilot


## 🚀 Objectives

- Design high-quality prompts using ReAct and Plan-Solve strategies
- Integrate function/tool-calling to mock scheduling and health tips retrieval
- Evaluate prompts using qualitative + quantitative metrics
- Deliver interactive UI and structured evaluation notebook

---


## 🧠 Core Features

- **Agent Reasoning:** ReAct and Plan-Solve prompt strategies
- **Tool Integration:** `get_diet_tip()`, `schedule_reminder()`
- **Prompt Evaluation:** Scored metrics across versions
- **UI (Optional):** Streamlit app to test responses interactively
- **Notebook:** Tracks prompt versions, live responses, and scores



## 🚀 
- ReAct (Reasoning + Action)
- Function/tool calling with tool chaining
- Multi-API integration





## 🧰 APIs Used
- [Nutritionix](https://developer.nutritionix.com/)
- [OpenFoodFacts](https://world.openfoodfacts.org/data)
- (Optional) CalorieNinjas, USDA FoodData



## 🛠️ Installation

```bash
git clone https://github.com/Agaramsaikrishna/Health-Copilot.git
cd Health-Copilot
pip install -r requirements.txt
```
💻 How to Use
1. Run Prompt Evaluations
bash
Copy
Edit
jupyter notebook notebooks/prompt_eval.ipynb
Tests prompt versions V1 → V4

Displays response comparisons

Outputs evaluation metrics

2. Start the UI 
bash
Copy
Edit
streamlit run app.py
Interactive chat to try different prompts

View scoring and reasoning trace


📊 Evaluation Metrics
Metric	Description
Accuracy	Correctness of the output
Coherence	Logical reasoning + fluency
Completeness	Whether all parts were addressed
Reasoning Used	Step-by-step or tool-aware logic
User-Friendliness	How readable the response was

Evaluation logic in eval/score.py.




## 🎯 Additional Next Steps

| Area | What You Can Do |
|------|------------------|
| RAG (Retrieval) | Use local health PDFs (e.g. WHO) with `langchain` |
| Analytics | Store all prompts and responses to a CSV log for review |
| Schedule Reminders | Integrate with Google Calendar mock or cron jobs |
| Improve UI | Add basic React or Streamlit frontend |
| Fitness Tips | Add tool `get_fitness_routine()` using mock or free API |

---

## 🧠 Complex Multi-Step Use Case Template

**Prompt:**  
“What is a healthy lunch and can you set a reminder to drink water at 2 PM?”

### ReAct Breakdown:
1. Plan: Identify lunch recommendation need → find nutritional guidance
2. Solve: Use `search_nutritionix_food`
3. Plan: Identify scheduling need → water reminder
4. Solve: Use `schedule_reminder("Drink water", "14:00")`
5. Reflect: Summarize both outcomes

---



## 📦 Deliverables

notebooks\prompt_version_evaluation.ipynb - All versions + evaluation

HealthCopilot\slides\Health_Copilot_A_Strategic_Evolution.pdf -slide presentation

Agent implementation with agno(phidata)/Tool use

Streamlit front-end 

Modular, documented codebase


## ✅ Final Checklist for Submission

| Requirement | ✅ |
|-------------|----|
| Tool calling for reminders & diet tips | ✅ |
| Multi-step ReAct reasoning | ✅ |
| At least 2 API integrations | ✅ |
| Evaluation framework (CSV/Sheet) | ✅ |
| Plagiarism-free, structured code | ✅ |
| Readme + docstrings + modular code | ✅ |

---


Would you like me to:
- ✅ Bundle and send a full zip with all code you need?
- ✅ Add `.env` and credential support for APIs?
- ✅ Create a React UI or Streamlit app template?

Let me know what you'd like help with next!
