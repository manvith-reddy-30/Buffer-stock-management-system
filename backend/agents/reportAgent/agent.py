import os
from dotenv import load_dotenv
from pathlib import Path

# Get path to agents/.env
env_path = Path(__file__).resolve().parents[2] / ".env"  # heart -> agents

# Load local agents/.env
load_dotenv(dotenv_path=env_path)

# Access the variable
MODEL = os.getenv("MODEL")

from google.adk.agents.llm_agent import LlmAgent
from prompt import PROMPT
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="report_agent",
    description="Analyzes tomato prices, weather, and buffer stock across 5 Telangana regions [HYDERABAD,MEDAK,NALGONDA,RANGAREDDY,WARANGAL] and provides logistics recommendations.",
    instruction=PROMPT,
    model=MODEL,
    tools=[google_search],
    output_key="buffer_stock_report",
)
