import streamlit as st
from agents.copilot_agent import copilot
from eval.scorer import score_response
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns





from agno.agent import Agent, RunResponse
from agno.models.together import Together
from agno.models.groq import Groq
from agno.tools.wikipedia import WikipediaTools
from utils.instructions import FIRST_instruction,prompt_eval_instruction, eval_instruction, eval_instructionA
from dotenv import load_dotenv
import os 
import json
from keys import *
from tools.health_risk import health_risk_assessment
from services.exercise import get_exercise_plan
from services.reminder import schedule_reminder
from services.evaluation import evaluate_response
from tools.nutrition_api import get_openfoodfacts_nutrition , search_nutritionix_food
from eval.eval_runner import get_eval_runner
from typing import Dict, List, Optional, Any

prompt_agent = Agent(
    model=Together(id=DISTILL_LLAMA_TOGETHER_AI_70B , api_key=TOGETHER_API_KEY),
    tools=[ health_risk_assessment, schedule_reminder , search_nutritionix_food , get_openfoodfacts_nutrition, get_exercise_plan ],
    description="You are a prompt generation and evaluation planner. Given a use case, generate a test prompt, expected keywords, and expected tools for evaluation.",
   #reasoning=True,
    show_tool_calls=False,
    instructions=prompt_eval_instruction
)




evaluator_agentA= Agent(
    model=Together(id=DISTILL_LLAMA_TOGETHER_AI_70B , api_key=TOGETHER_API_KEY),
    tools=[prompt_agent ,  get_eval_runner],
    description="You are an evaluation controller agent that generates prompts and scores copilot responses .",
    show_tool_calls=False,
    instructions=eval_instructionA
)

# evaluator_agentA.print_response("Evaluate how the copilot helps an overweight smoker reduce risk.")



evaluator_agent= Agent(
    model=Together(id=DISTILL_LLAMA_TOGETHER_AI_70B , api_key=TOGETHER_API_KEY),
    tools=[get_eval_runner],
    description="You are an evaluation controller agent that phrase prompts and scores copilot responses.",
    show_tool_calls=False,
    instructions=eval_instruction
)




# ========== PAGE CONFIG ==========
st.set_page_config(page_title="🧪 Copilot Evaluator", layout="wide")
st.title("🧠 Preventive Health Copilot Evaluation Dashboard")
st.markdown("An interactive dashboard to analyze the quality and effectiveness of AI-generated responses.")
st.markdown("---")

# ========== SESSION STATE ==========
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========== SIDEBAR ==========
st.sidebar.title("⚙️ Mode Selector")
mode = st.sidebar.radio("Choose a Mode", [ "Auto Evaluation","Manual Evaluation", "Copilot Chat"])



# ========== MODE 1 : Auto Evaluation ==========
if mode == "Auto Evaluation":
    st.header("🤖 Auto Generate & Evaluate Prompt")
    st.info("Click the button below to auto-generate a prompt using internal logic and evaluate it.")

    if st.button("🎯 Generate Prompt & Evaluate"):
        try:
            with st.spinner("🧪 Running internal prompt generation and evaluation..."):
                run_response = evaluator_agentA.run()  # Your agent does everything
                response = run_response.content.strip()

            st.success("✅ Evaluation Complete")
            st.markdown("### 🧾 Evaluation Result")
            st.markdown(f"**Copilot Evaluation:**\n\n{response}")

            

        except Exception as e:
            st.error(f"❌ Evaluation failed: {e}")



# ========== MODE 2 # # : Manual Evaluation ==========
if mode == "Manual Evaluation":
    st.header("🔧 Manual Prompt Evaluation")
    st.info("Fill out the fields below to manually evaluate a Copilot prompt.")

    prompt_text = st.text_area("📝 Prompt", height=150, placeholder="E.g., Suggest diet for someone with high cholesterol and low activity.")
    expected_keywords = st.text_input("🔑 Expected Keywords (comma-separated)", placeholder="fiber, oats, unsaturated fat")
    expected_tools = st.multiselect("🛠 Expected Tools", options=[
        "health_risk_assessment",
        "schedule_reminder",
        "search_nutritionix_food",
        "get_openfoodfacts_nutrition",
        "get_exercise_plan"
    ])

    if st.button("Run Manual Evaluation"):
        if not prompt_text:
            st.warning("Please enter a prompt.")
        else:
            try:
                prompt_data = {
                    "prompt": prompt_text,
                    "expected_keywords": [k.strip() for k in expected_keywords.split(",") if k.strip()],
                    "expected_tools": expected_tools
                }
                with st.spinner("Evaluating..."):
                    result = evaluator_agent.run(prompt_data)
                  
                response=result.content.strip()
                st.success("✅ Evaluation complete.")
                st.markdown(f"**Copilot Evaluation:**\n\n{response}")

                #t.download_button("📥 Download Result as JSON", data=json.dumps(result, indent=2), file_name="manual_eval_result.json")
            except Exception as e:
                st.error(f"❌ Error during evaluation: {e}")




# ========== MODE 3: Copilot Chat ==========
elif mode == "Copilot Chat":
    st.header("💬 Chat with Preventive Health Copilot")
    st.info("Ask any preventive health question. The system will respond directly.")

    chat_query = st.text_area("Your Question", height=100, placeholder="e.g., What's a good exercise for someone with high blood pressure?")
    if st.button("Send to Copilot"):
        if not chat_query.strip():
            st.warning("Please type a question.")
        else:
            with st.spinner("Getting response..."):
                try:
                    run_response = copilot.run(chat_query)
                    response = run_response.content.strip()

                    # # Save to chat history
                    # st.session_state.chat_history.append({
                    #     "user": chat_query,
                    #     "copilot": response
                    # })

                    st.success("✅ Response received.")
                    st.markdown(f"**🧠 Copilot:** {response}")

                except Exception as e:
                    st.error(f"❌ Copilot error: {e}")





df=pd.read_csv("data\evaluation_results.csv")

# =============================================================================
# DATA LOADING
# Use @st.cache_data to load the data once and cache it.
# =============================================================================
@st.cache_data
def load_data(file_path):
    """
    Loads evaluation data from a CSV file.
    Includes error handling for a missing file.
    """
    try:
        df = pd.read_csv(file_path)
        # Convert Yes/No columns to boolean for easier calculations if needed
        for col in ['Accuracy', 'Coherence', 'Completeness', 'User-Friendliness', 'Reasoning Used']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
        return df
    except FileNotFoundError:
        st.error(f"❌ **File not found:** Make sure your `evaluation_results.csv` is in the `{file_path.parent}` directory.")
        return None
# =============================================================================
# DATA LOADING (with fixed file path)
# =============================================================================
@st.cache_data
def load_data():
    """Loads evaluation data from the CSV file."""
    try:
        # Use forward slashes for cross-platform compatibility
        file_path = "data/evaluation_results.csv"
        df = pd.read_csv(file_path)
        # Clean up data for consistency
        for col in ['Accuracy', 'Coherence', 'Completeness', 'User-Friendliness', 'Reasoning Used']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
        return df
    except FileNotFoundError:
        st.error(f"❌ **File not found:** Please make sure `evaluation_results.csv` is in the `data/` directory.")
        return None

# =============================================================================
# MAIN DASHBOARD UI
# =============================================================================

st.markdown("---")

# Load the data
df = load_data()

# Only display the dashboard if the data was loaded successfully
if df is not None:

    # --- 1. HIGH-LEVEL KPIs ---
    st.subheader("Key Performance Indicators (KPIs)")
    col1, col2, col3 = st.columns(3)
    avg_score = df['Score (0–5)'].mean()
    accuracy_rate = (df['Accuracy'] == 'yes').mean() * 100
    reasoning_rate = (df['Reasoning Used'] == 'yes').mean() * 100

    col1.metric("Average Score", f"{avg_score:.2f} / 5")
    col2.metric("Overall Accuracy", f"{accuracy_rate:.1f}%")
    col3.metric("Reasoning Used Rate", f"{reasoning_rate:.1f}%")
    st.markdown("---")

    # --- 2. VISUAL ANALYSIS ---
    st.subheader("Visual Analysis")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### Score Distribution")
        # Use Streamlit's native bar chart for interactivity
        st.bar_chart(df['Score (0–5)'].value_counts())

    with chart_col2:
        # --- FIXED CORRELATION HEATMAP ---
        st.markdown("##### Correlation of Metrics")
        
        # 1. Identify the columns with text
        cols_to_convert = ['Accuracy', 'Coherence', 'Completeness', 'User-Friendliness', 'Reasoning Used']

        # 2. Create a new numeric DataFrame for correlation
        numeric_df = df[cols_to_convert].apply(lambda s: s.map({'yes': 1, 'no': 0}))

        # 3. Now, calculate the correlation on the purely numeric data
        correlation = numeric_df.corr()

        # 4. Create the heatmap
        fig, ax = plt.subplots()
        sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
        st.pyplot(fig)
        
    st.markdown("---")

    # --- 3. DETAILED DATA TABLE ---
    st.subheader("Detailed Evaluation Results")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- 4. FAILURE ANALYSIS ---
    with st.expander("🚨 **Weakest Prompts Analysis (Score <= 2.0)**"):
        weak_prompts = df[df['Score (0–5)'] <= 2.0]
        if weak_prompts.empty:
            st.success("No prompts scored 2.0 or less. Great job!")
        else:
            st.warning(f"Found **{len(weak_prompts)}** prompts that require immediate improvement.")
            st.dataframe(
                weak_prompts[['Prompt', 'Score (0–5)', 'Accuracy', 'Reasoning Used']], 
                use_container_width=True, 
                hide_index=True
            )