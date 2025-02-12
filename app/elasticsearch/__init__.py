from elasticsearch import Elasticsearch

from app.config import get_settings


def get_client() -> Elasticsearch:
    return Elasticsearch(get_settings().ES_HOST)
