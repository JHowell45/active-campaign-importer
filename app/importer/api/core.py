from app.config import get_settings


def get_headers() -> dict:
    return {
        "accept": "application/json",
        "Api-Token": get_settings().ACTIVE_CAMPAIGN_API_TOKEN,
    }
