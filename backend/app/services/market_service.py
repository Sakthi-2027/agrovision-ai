import requests
from flask import current_app

MARKET_API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


def get_market_prices(state=None, commodity=None, limit=20):
    """Fetches live mandi prices, optionally filtered by state and/or commodity."""
    params = {
        "api-key": current_app.config["DATA_GOV_API_KEY"],
        "format": "json",
        "limit": limit
    }

    if state:
        params["filters[state]"] = state
    if commodity:
        params["filters[commodity]"] = commodity

    response = requests.get(MARKET_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("records", [])