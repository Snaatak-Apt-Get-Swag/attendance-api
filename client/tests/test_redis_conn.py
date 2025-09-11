import os
from unittest import mock
import pytest
from client.redis import MiddlewareSDKFacade
from client.redis.redis_conn import get_caching_data

@pytest.fixture
def mock_config_file():
    mock_file = mock.MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = """
    redis:
        host: localhost
        port: 6379
        password: mypassword
    """
    return mock_file

@mock.patch("client.redis.open")
def test_get_caching_data(mock_open, mock_config_file):
    mock_open.return_value = mock_config_file
    os.environ["CONFIG_FILE"] = "config.yaml"

    result = get_caching_data()

    # Assert structure and values
    assert result["CACHE_TYPE"] == "redis"
    assert result["CACHE_REDIS_PORT"] == 6379
    assert "CACHE_REDIS_HOST" in result
    assert result["CACHE_REDIS_URL"].startswith(f"redis://{result['CACHE_REDIS_HOST']}")

    del os.environ["CONFIG_FILE"]

def test_redis_status():
    # redis_status() mocked by conftest.py
    redis_client = MiddlewareSDKFacade.cache.redis_status()
    assert redis_client == "up"
