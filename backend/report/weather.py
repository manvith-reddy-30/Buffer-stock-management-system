import os
from dotenv import load_dotenv
from pathlib import Path

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Load model (optional if needed elsewhere)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Session details
APP_NAME = "weather_report"
USER_ID = "weather_user"
session_service = InMemorySessionService()

# Import weather agents
from agents.weatherAgent.hyderabad.agent import root_agent as hyderabad_weather
from agents.weatherAgent.nalgonda.agent import root_agent as nalgonda_weather
from agents.weatherAgent.warangal.agent import root_agent as warangal_weather
from agents.weatherAgent.medak.agent import root_agent as medak_weather
from agents.weatherAgent.rangareddy.agent import root_agent as rangareddy_weather


# Mapping from place name to agent
AGENT_MAP = {
    "hyderabad": hyderabad_weather,
    "nalgonda": nalgonda_weather,
    "warangal": warangal_weather,
    "medak": medak_weather,
    "rangareddy": rangareddy_weather,
}


async def weather_report(place: str) -> str:
    """
    Fetches a clean 7-day weather report for the given district name.
    Returns a formatted string, or an error message if place is invalid or data is missing.
    """
    place = place.lower()
    agent = AGENT_MAP.get(place)

    if not agent:
        return f"❌ No weather agent available for '{place}'"

    session_id = f"{place}_weather_session"

    # Prepare the query format
    query = (
        "Provide a 7-day weather forecast in the following format:\n"
        "# Day, Month Date, Year: Morning condition, Evening condition, "
        "Morning rain chance, Evening rain chance, Min-Max temperature in °C, Humidity %\n"
        "Use one line per day, and include exact weather terms like 'Cloudy', 'Light rain', etc.\n"
        "Example:\n"
        "# Sunday, June 29, 2025: Light rain, Cloudy, 40% chance of rain, 25% chance of rain, 24-32°C, 66% humidity"
    )

    # Create session and run the agent
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )

    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=query)])

    for _ in runner.run(user_id=USER_ID, session_id=session_id, new_message=content):
        pass

    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    return session.state.get(
        f"{place}_weather", f"No weather data returned for '{place}'"
    )
