import pytest
from unittest.mock import patch, MagicMock

# ---------------- Mock Postgres ----------------
def _mock_psycopg2_connect(*args, **kwargs):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # Example fake results
    mock_cursor.fetchone.return_value = {"id": "1", "name": "John Doe", "status": "Present", "date": "2023-01-01"}
    mock_cursor.fetchall.return_value = [
        {"id": "1", "name": "John Doe", "status": "Present", "date": "2023-01-01"},
        {"id": "2", "name": "Jane Smith", "status": "Absent", "date": "2023-01-02"},
    ]
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

# ---------------- Mock Redis ----------------
def _mock_redis_client(*args, **kwargs):
    mock_redis = MagicMock()
    mock_redis.get.return_value = "value"
    mock_redis.set.return_value = True
    mock_redis.ping.return_value = True
    return mock_redis

# ---------------- Auto Apply Mocks ----------------
@pytest.fixture(autouse=True, scope="session")
def mock_db_and_cache():
    """Automatically mock Postgres & Redis for all tests."""
    with patch("psycopg2.connect", side_effect=_mock_psycopg2_connect), \
         patch("redis.Redis", side_effect=_mock_redis_client), \
         patch("redis.StrictRedis", side_effect=_mock_redis_client):
        yield
