import os
from dotenv import load_dotenv
from pathlib import Path

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Load .env for model info
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)
MODEL = os.getenv("MODEL")

# Import weather agents
from agents.weatherAgent.hyderabad.agent import root_agent as hyderabad_weather
from agents.weatherAgent.nalgonda.agent import root_agent as nalgonda_weather
from agents.weatherAgent.warangal.agent import root_agent as warangal_weather
from agents.weatherAgent.medak.agent import root_agent as medak_weather
from agents.weatherAgent.rangareddy.agent import root_agent as rangareddy_weather

# Constants
APP_NAME = "hyderabad_buffer_report"
USER_ID = "buffer_user"
SESSION_ID = "buffer_session"
session_service = InMemorySessionService()

# Define report agent
PROMPT = """
You are a supply chain analyst focused on agricultural planning. Your task is to generate a detailed buffer stock management report for **Hyderabad**, focusing on tomato supply.

You are provided with:
- **Actual tomato prices from the past week** for Hyderabad, Nalgonda, Rangareddy, Medak, and Warangal.
- **Predicted tomato prices for the next 7 days** for these districts.
- **Current buffer stock levels (in tons)** for each of the above districts.
- **Weather forecasts** for all districts.

Your objectives are:
1. Analyze **Hyderabad’s** tomato price trends using both actual and predicted data.
2. Evaluate **weather conditions** and their potential impact on supply and demand in Hyderabad.
3. Use buffer stock levels and price trends from **neighboring districts** (Nalgonda, Rangareddy, Medak, Warangal) to assess potential:
   - **Risks or opportunities** for Hyderabad’s buffer planning.
   - **Inter-district mobilization** if needed (e.g., if another district has excess stock and stable prices).
4. Provide a recommendation on:
   - Whether Hyderabad’s buffer is **sufficient, excessive, or insufficient**.
   - Any **action plan** (e.g., procure more stock, transfer from other regions, reduce storage).
5. Keep the focus of the analysis on Hyderabad, but use the other districts for supporting context.

The final report must be:
- **Clear, structured, and actionable**.
- Written in plain language for agricultural officers or planning teams.
- Conclude with a brief summary of your recommendation.

Output the report as a structured text under the key `buffer_stock_report`.
"""

root_agent = LlmAgent(
    name="report_agent",
    description="Analyzes and generates the report for hyderabad based upon the last week actual tomato prices and next week predicted prices and weather reports",
    instruction=PROMPT,
    model=MODEL,
    tools=[google_search],
    output_key="buffer_stock_report",
)


async def hyderabad_report(
    hyderabad_last_week_actual,
    hyderabad_next_week_pred,
    nalgonda_last_week_actual,
    nalgonda_next_week_pred,
    rangareddy_last_week_actual,
    rangareddy_next_week_pred,
    medak_last_week_actual,
    medak_next_week_pred,
    warangal_last_week_actual,
    warangal_next_week_pred,
    buffer_quantity,
):
    # Get weather data from agents
    async def get_weather(weather_agent, key):
        session_id = f"{key}_weather_session"

        await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

        query = (
            "Provide a 7-day weather forecast in the following format:\n"
            "# Day, Month Date, Year: Morning condition, Evening condition, "
            "Morning rain chance, Evening rain chance, Min-Max temperature in °C, Humidity %\n"
            "Use one line per day, and include exact weather terms like 'Cloudy', 'Light rain', etc.\n"
            "Example:\n"
            "# Sunday, June 29, 2025: Light rain, Cloudy, 40% chance of rain, 25% chance of rain, 24-32°C, 66% humidity"
        )

        runner = Runner(
            agent=weather_agent, app_name=APP_NAME, session_service=session_service
        )
        content = types.Content(role="user", parts=[types.Part(text=query)])

        for _ in runner.run(
            user_id=USER_ID, session_id=session_id, new_message=content
        ):
            pass

        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
        return session.state.get(f"{key}_weather", f"No weather data for {key}")

    # Fetch weather reports
    hyderabad_weather_report = await get_weather(hyderabad_weather, "hyderabad")
    nalgonda_weather_report = await get_weather(nalgonda_weather, "nalgonda")
    rangareddy_weather_report = await get_weather(rangareddy_weather, "rangareddy")
    medak_weather_report = await get_weather(medak_weather, "medak")
    warangal_weather_report = await get_weather(warangal_weather, "warangal")

    # Format helper
    def format_prices(label, last_week, next_week):
        return (
            f"\n**{label}**:\n"
            f"- Past 7 days actual prices (index 0 = 7 days ago, 6 = yesterday): {last_week}\n"
            f"- Next 7 days predicted prices (index 0 = today, 6 = 6 days ahead): {next_week}\n"
        )

    # Construct the input query to LLM
    query = (
        "**🛑 Hyderabad Tomato Buffer Stock Analysis**\n\n"
        "_Note: For actual prices, index 0 = 7 days ago → index 6 = yesterday. For predicted prices, index 0 = today → index 6 = 6 days from now._\n\n"
        "**📊 Price Data:**\n"
        + format_prices(
            "Hyderabad", hyderabad_last_week_actual, hyderabad_next_week_pred
        )
        + format_prices("Nalgonda", nalgonda_last_week_actual, nalgonda_next_week_pred)
        + format_prices(
            "Rangareddy", rangareddy_last_week_actual, rangareddy_next_week_pred
        )
        + format_prices("Medak", medak_last_week_actual, medak_next_week_pred)
        + format_prices("Warangal", warangal_last_week_actual, warangal_next_week_pred)
        + "\n**🧊 Current Buffer Stock (in tons):**\n"
        f"- Hyderabad: {buffer_quantity['hyderabad']}\n"
        f"- Nalgonda: {buffer_quantity['nalgonda']}\n"
        f"- Rangareddy: {buffer_quantity['rangareddy']}\n"
        f"- Medak: {buffer_quantity['medak']}\n"
        f"- Warangal: {buffer_quantity['warangal']}\n" + "\n**🌦️ Weather Forecasts:**\n"
        f"- Hyderabad: {hyderabad_weather_report}\n"
        f"- Nalgonda: {nalgonda_weather_report}\n"
        f"- Rangareddy: {rangareddy_weather_report}\n"
        f"- Medak: {medak_weather_report}\n"
        f"- Warangal: {warangal_weather_report}\n"
    )

    # Run the agent
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )
    content = types.Content(role="user", parts=[types.Part(text=query)])

    for _ in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        pass

    # Retrieve the weather response from agent session state
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    return session.state.get("buffer_stock_report", "No report generated.")
