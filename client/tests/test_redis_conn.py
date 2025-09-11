import os
import pytest
from client.redis import MiddlewareSDKFacade
from client.redis.redis_conn import get_caching_data

# -----------------------------
# Test for reading Redis config
# -----------------------------
def test_get_caching_data():
    # Assuming CONFIG_FILE env variable points to your real config
    os.environ["CONFIG_FILE"] = "config.yaml"

    result = get_caching_data()

    # Assert structure and values
    assert result["CACHE_TYPE"] == "redis"
    assert result["CACHE_REDIS_PORT"] == 6379
    assert "CACHE_REDIS_HOST" in result
    assert result["CACHE_REDIS_URL"].startswith(f"redis://{result['CACHE_REDIS_HOST']}")

    del os.environ["CONFIG_FILE"]


# -----------------------------
# Test for Redis status
# -----------------------------
def test_redis_status():
    redis_client_status = MiddlewareSDKFacade.cache.redis_status()
    
    # Redis should be reachable
    assert redis_client_status == "up"
