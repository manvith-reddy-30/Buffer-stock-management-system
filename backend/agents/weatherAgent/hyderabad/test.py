from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from tenacity import retry, wait_fixed

APP_NAME = "weather_app"
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
                session.state.get("hyderabad_weather"),
            )


async def main():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    await call_agent()


if __name__ == "__main__":
    asyncio.run(main())
