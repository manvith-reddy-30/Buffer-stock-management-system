import os
from dotenv import load_dotenv
from pathlib import Path

# Get path to agents/.env
env_path = Path(__file__).resolve().parents[3] / ".env"  # heart -> agents

# Load local agents/.env
load_dotenv(dotenv_path=env_path)

# Access the variable
MODEL = os.getenv("MODEL")

from google.adk.agents.llm_agent import LlmAgent
from agents.weatherAgent.rangareddy.prompt import PROMPT
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="rangareddy_weather_agent",
    description=(
        "This agent provides weather report of rangareddy district  of telangana state ,india."
    ),
    instruction=PROMPT,
    model=MODEL,
    tools=[google_search],
    output_key="rangareddy_weather",
)
