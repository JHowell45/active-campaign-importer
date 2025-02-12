from typing import Type, TypeVar

import requests

from app.config import get_settings
from app.importer.api.core import get_headers

T = TypeVar("T")


def pagination(
    endpoint: str,
    response_type: Type[T],
    page: int = 0,
    limit: int = 10,
    filters: dict | None = None,
) -> T:
    url = f"https://{get_settings().ACTIVE_CAMPAIGN_ACCOUNT_NAME}.api-us1.com/api/3/{endpoint}?limit={limit}&offset={page * limit}"
    if filters is not None:
        url += "".join(["&filters[{key}]={value}" for key, value in filters.items()])
    r = requests.get(url, headers=get_headers())
    return response_type(**r.json())
