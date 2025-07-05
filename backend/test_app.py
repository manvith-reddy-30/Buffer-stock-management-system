import pytest
from httpx import AsyncClient
from fastapi import FastAPI

# Assuming this is your main FastAPI app file
from backend.main import (
    app,
)  # Adjust the import if your app entry point is named differently

# Sample mock input data
mock_data = {
    "hyderabad": {
        "last_week_actual": [24, 25, 26, 25, 27, 26, 25],
        "next_week_pred": [26, 27, 28, 28, 29, 30, 31],
    },
    "nalgonda": {
        "last_week_actual": [23, 24, 25, 25, 26, 25, 24],
        "next_week_pred": [25, 26, 27, 27, 28, 29, 30],
    },
    "rangareddy": {
        "last_week_actual": [22, 23, 23, 24, 24, 25, 25],
        "next_week_pred": [25, 25, 26, 27, 27, 28, 28],
    },
    "medak": {
        "last_week_actual": [21, 22, 22, 23, 24, 24, 25],
        "next_week_pred": [24, 25, 26, 26, 27, 28, 29],
    },
    "warangal": {
        "last_week_actual": [26, 27, 27, 28, 28, 29, 30],
        "next_week_pred": [30, 31, 31, 32, 32, 33, 33],
    },
    "buffer_quantity": {
        "hyderabad": 150,
        "nalgonda": 120,
        "rangareddy": 130,
        "medak": 100,
        "warangal": 180,
    },
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "district", ["hyderabad", "nalgonda", "rangareddy", "medak", "warangal"]
)
async def test_analysis_endpoints(district):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            f"{district}_last_week_actual": mock_data[district]["last_week_actual"],
            f"{district}_next_week_pred": mock_data[district]["next_week_pred"],
        }

        # Add other districts' data depending on which endpoint is being tested
        for other in ["hyderabad", "nalgonda", "rangareddy", "medak", "warangal"]:
            if other != district:
                payload[f"{other}_last_week_actual"] = mock_data[other][
                    "last_week_actual"
                ]
                payload[f"{other}_next_week_pred"] = mock_data[other]["next_week_pred"]

        payload["buffer_quantity"] = mock_data["buffer_quantity"]

        response = await ac.post(f"/analysis/{district}", json=payload)
        assert response.status_code == 200
        assert "buffer_stock_report" in response.json()
        assert isinstance(response.json()["buffer_stock_report"], str)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "district", ["hyderabad", "nalgonda", "rangareddy", "medak", "warangal"]
)
async def test_weather_endpoints(district):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/weather/{district}")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "forecast" in response.json()
        assert isinstance(response.json()["forecast"], str)
