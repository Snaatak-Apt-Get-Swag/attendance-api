import os
from unittest import mock
import pytest
from client.redis import MiddlewareSDKFacade
from client.redis.redis_conn import get_caching_data

# Use a fixture for mock config file
@pytest.fixture
def mock_config():
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
def test_get_caching_data(mock_open, mock_config):
    mock_open.return_value = mock_config
    os.environ["CONFIG_FILE"] = "config.yaml"

    result = get_caching_data()

    # Dynamically read host from config (mocked as 'localhost')
    expected_host = "localhost"
    expected = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": expected_host,
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_URL": f"redis://{expected_host}:6379/0",
    }

    assert result == expected

    del os.environ["CONFIG_FILE"]


@mock.patch("client.redis.open")
def test_redis_status(mock_open, mock_config):
    mock_open.return_value = mock_config
    os.environ["CONFIG_FILE"] = "config.yaml"

    redis_client = MiddlewareSDKFacade.cache.redis_status()

    assert redis_client == "up"

    del os.environ["CONFIG_FILE"]
