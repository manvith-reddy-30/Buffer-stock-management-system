from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from tenacity import retry, wait_fixed

APP_NAME = "report_app"
USER_ID = "user_01"
SESSION_ID = "test_session"

from agent import root_agent

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


@retry(wait=wait_fixed(5))
async def call_agent(query=None):
    if query is None:
        query = (
            "Give a 7-day detailed weather forecast for Hyderabad, Telangana, India, "
            "starting today. The report should include daily rain chances, temperature range, "
            "and humidity. The forecast should help farmers and buffer stock managers assess "
            "potential risks of tomato price crashes due to excess rainfall or extreme weather. "
            "Provide the report in plain text format, one day per line, with clean details like: "
            "date, day, weather condition, temperature range (°C), rain chance (%), and humidity (%)."
        )

    print("\n" + "=" * 50)
    print(f"Input: {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            session = await session_service.get_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
            )
            print(
                "session state dot bot_response:",
                session.state.get("buffer_stock_report"),
            )


async def main():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    await call_agent("""
REGION: Hyderabad
Last 7 Prices: 980, 970, 950, 930, 910, 920, 900
Next 7 Predictions: 870, 850, 820, 800, 780, 760, 740
Weather:
Sunday, June 29, 2025: Light rain, Cloudy, 40% chance of rain, 25% chance of rain, 24-32°C, 66% humidity
Monday, June 30, 2025: Cloudy, Cloudy, 20% chance of rain, 25% chance of rain, 24-31°C, 66% humidity
Tuesday, July 1, 2025: Light rain, Light rain, 35% chance of rain, 40% chance of rain, 24-29°C, 68% humidity
Wednesday, July 2, 2025: Light rain, Cloudy, 35% chance of rain, 10% chance of rain, 24-29°C, 72% humidity
Thursday, July 3, 2025: Cloudy, Cloudy, 20% chance of rain, 10% chance of rain, 24-29°C, 70% humidity
Friday, July 4, 2025: Cloudy, Cloudy, 20% chance of rain, 10% chance of rain, 24-29°C, 71% humidity
Saturday, July 5, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 24-29°C, 70% humidity
Buffer Stock: 45 tons

REGION: Warangal
Last 7 Prices: 1100, 1120, 1150, 1180, 1200, 1220, 1240
Next 7 Predictions: 1260, 1290, 1320, 1350, 1370, 1400, 1420
Weather:
Sunday, June 29, 2025: Clear, Clear, 0% chance of rain, 0% chance of rain, 26-34°C, 55% humidity
Monday, June 30, 2025: Clear, Clear, 0% chance of rain, 0% chance of rain, 26-35°C, 52% humidity
Tuesday, July 1, 2025: Partly cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 25-34°C, 54% humidity
Wednesday, July 2, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 25-33°C, 58% humidity
Thursday, July 3, 2025: Cloudy, Light rain, 15% chance of rain, 20% chance of rain, 24-32°C, 60% humidity
Friday, July 4, 2025: Light rain, Cloudy, 20% chance of rain, 15% chance of rain, 24-31°C, 62% humidity
Saturday, July 5, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 24-30°C, 59% humidity
Buffer Stock: 20 tons

REGION: Medak
Last 7 Prices: 870, 890, 860, 850, 840, 820, 800
Next 7 Predictions: 810, 820, 830, 820, 810, 800, 790
Weather:
Sunday, June 29, 2025: Light rain, Cloudy, 45% chance of rain, 30% chance of rain, 24-31°C, 72% humidity
Monday, June 30, 2025: Cloudy, Cloudy, 30% chance of rain, 20% chance of rain, 24-30°C, 70% humidity
Tuesday, July 1, 2025: Rain, Rain, 60% chance of rain, 50% chance of rain, 23-29°C, 75% humidity
Wednesday, July 2, 2025: Light rain, Cloudy, 35% chance of rain, 20% chance of rain, 24-29°C, 73% humidity
Thursday, July 3, 2025: Cloudy, Cloudy, 20% chance of rain, 10% chance of rain, 24-29°C, 70% humidity
Friday, July 4, 2025: Cloudy, Cloudy, 15% chance of rain, 10% chance of rain, 24-29°C, 68% humidity
Saturday, July 5, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 24-29°C, 69% humidity
Buffer Stock: 50 tons

REGION: NALGONDA
Last 7 Prices: 1020, 1000, 980, 970, 960, 950, 940
Next 7 Predictions: 930, 910, 890, 870, 860, 850, 830
Weather:
Sunday, June 29, 2025: Cloudy, Cloudy, 15% chance of rain, 15% chance of rain, 25-33°C, 62% humidity
Monday, June 30, 2025: Cloudy, Light rain, 25% chance of rain, 30% chance of rain, 24-32°C, 64% humidity
Tuesday, July 1, 2025: Light rain, Rain, 40% chance of rain, 55% chance of rain, 23-30°C, 68% humidity
Wednesday, July 2, 2025: Light rain, Cloudy, 35% chance of rain, 20% chance of rain, 24-29°C, 70% humidity
Thursday, July 3, 2025: Cloudy, Cloudy, 20% chance of rain, 10% chance of rain, 24-30°C, 65% humidity
Friday, July 4, 2025: Cloudy, Cloudy, 15% chance of rain, 10% chance of rain, 25-30°C, 64% humidity
Saturday, July 5, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 24-30°C, 63% humidity
Buffer Stock: 25 tons

REGION: RANGAREDDY
Last 7 Prices: 1150, 1130, 1120, 1100, 1080, 1060, 1050
Next 7 Predictions: 1030, 1010, 990, 980, 960, 940, 920
Weather:
Sunday, June 29, 2025: Light rain, Light rain, 50% chance of rain, 40% chance of rain, 24-31°C, 70% humidity
Monday, June 30, 2025: Cloudy, Cloudy, 30% chance of rain, 25% chance of rain, 24-31°C, 68% humidity
Tuesday, July 1, 2025: Light rain, Cloudy, 35% chance of rain, 20% chance of rain, 24-30°C, 69% humidity
Wednesday, July 2, 2025: Cloudy, Cloudy, 25% chance of rain, 15% chance of rain, 24-30°C, 66% humidity
Thursday, July 3, 2025: Cloudy, Cloudy, 20% chance of rain, 10% chance of rain, 24-30°C, 65% humidity
Friday, July 4, 2025: Cloudy, Cloudy, 15% chance of rain, 10% chance of rain, 24-30°C, 64% humidity
Saturday, July 5, 2025: Cloudy, Cloudy, 10% chance of rain, 10% chance of rain, 24-30°C, 63% humidity
Buffer Stock: 35 tons
""")


if __name__ == "__main__":
    asyncio.run(main())
