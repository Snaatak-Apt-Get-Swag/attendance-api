# conftest.py
import pytest
from unittest.mock import patch, MagicMock


# ---------------- Mock Postgres ----------------
def _mock_psycopg2_connect(*args, **kwargs):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Fake query results
    mock_cursor.fetchone.return_value = ("mocked_result",)
    mock_cursor.fetchall.return_value = [("row1",), ("row2",)]
    mock_conn.cursor.return_value = mock_cursor

    return mock_conn


# ---------------- Mock Redis ----------------
def _mock_redis_client(*args, **kwargs):
    mock_redis = MagicMock()
    store = {}

    def mock_get(key):
        return store.get(key, None)

    def mock_set(key, value):
        store[key] = value
        return True

    mock_redis.get.side_effect = mock_get
    mock_redis.set.side_effect = mock_set
    mock_redis.ping.return_value = True

    return mock_redis


# ---------------- Apply Auto Fixtures ----------------
# Commenting out to use real Postgres & Redis
# @pytest.fixture(autouse=True, scope="session")
# def mock_db_and_cache():
#     """Automatically mock Postgres & Redis for all tests."""
#     with patch("psycopg2.connect", side_effect=_mock_psycopg2_connect), \
#          patch("redis.Redis", side_effect=_mock_redis_client), \
#          patch("redis.StrictRedis", side_effect=_mock_redis_client):
#         yield


def pytest_configure(config):
    """Hook to ensure mocks are active before imports."""
    # Comment out patching for real API usage
    # patch("psycopg2.connect", side_effect=_mock_psycopg2_connect).start()
    # patch("redis.Redis", side_effect=_mock_redis_client).start()
    # patch("redis.StrictRedis", side_effect=_mock_redis_client).start()
