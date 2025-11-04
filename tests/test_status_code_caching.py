"""Tests for conditional caching based on HTTP status codes."""
import time
from typing import Any, Generator

import pytest
from fastapi import FastAPI, HTTPException
from starlette.testclient import TestClient

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache


@pytest.fixture(autouse=False)
def reset_cache() -> Generator[Any, Any, None]:
    """Reset cache between tests."""
    FastAPICache.reset()
    yield
    FastAPICache.reset()


def test_cache_only_successful_status_codes(reset_cache: Any) -> None:
    """Test that only 2xx status codes are cached when configured."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=range(200, 300))
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/success")
    @cache(expire=60)
    async def success_endpoint() -> dict[str, int]:
        call_count["count"] += 1
        return {"value": call_count["count"]}
    
    @app.get("/error")
    @cache(expire=60)
    async def error_endpoint() -> dict[str, int]:
        call_count["count"] += 1
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    with TestClient(app) as client:
        # First request to success endpoint - should cache
        response1 = client.get("/success")
        assert response1.status_code == 200
        assert response1.json()["value"] == 1
        assert response1.headers.get("X-FastAPI-Cache") == "MISS"
        
        # Second request - should use cache
        response2 = client.get("/success")
        assert response2.status_code == 200
        assert response2.json()["value"] == 1
        assert response2.headers.get("X-FastAPI-Cache") == "HIT"
        
        # Reset counter for error endpoint
        call_count["count"] = 0
        
        # First request to error endpoint - should NOT cache
        response3 = client.get("/error")
        assert response3.status_code == 500
        assert call_count["count"] == 1
        
        # Second request - should NOT use cache (call function again)
        response4 = client.get("/error")
        assert response4.status_code == 500
        assert call_count["count"] == 2


def test_cache_specific_status_codes(reset_cache: Any) -> None:
    """Test caching specific status codes using a list."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=[200, 201, 404])
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/item")
    @cache(expire=60)
    async def get_item() -> dict[str, Any]:
        call_count["count"] += 1
        if call_count["count"] == 1:
            return {"found": True, "count": call_count["count"]}
        raise HTTPException(status_code=404, detail="Not found")
    
    with TestClient(app) as client:
        # First request returns 200 - should cache
        response1 = client.get("/item")
        assert response1.status_code == 200
        assert response1.headers.get("X-FastAPI-Cache") == "MISS"
        
        # Second request - should use cache
        response2 = client.get("/item")
        assert response2.status_code == 200
        assert response2.headers.get("X-FastAPI-Cache") == "HIT"
        assert response2.json()["count"] == 1


def test_per_endpoint_status_code_override(reset_cache: Any) -> None:
    """Test that per-endpoint status codes override global configuration."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=range(200, 300))
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/default")
    @cache(expire=60)
    async def default_endpoint() -> dict[str, int]:
        call_count["count"] += 1
        if call_count["count"] > 1:
            raise HTTPException(status_code=500, detail="Error")
        return {"value": call_count["count"]}
    
    @app.get("/custom")
    @cache(expire=60, cache_status_codes=[200, 500])
    async def custom_endpoint() -> dict[str, int]:
        call_count["count"] += 1
        raise HTTPException(status_code=500, detail="Error")
    
    with TestClient(app) as client:
        # Default endpoint with 500 should NOT cache (global config)
        call_count["count"] = 0
        response1 = client.get("/default")
        assert response1.status_code == 200
        
        response2 = client.get("/default")
        assert response2.status_code == 500
        assert call_count["count"] == 2  # Called twice, no cache
        
        # Custom endpoint with 500 SHOULD cache (endpoint config)
        call_count["count"] = 0
        response3 = client.get("/custom")
        assert response3.status_code == 500
        
        response4 = client.get("/custom")
        assert response4.status_code == 500
        assert call_count["count"] == 1  # Called once, used cache


def test_cache_all_status_codes_by_default(reset_cache: Any) -> None:
    """Test that all status codes are cached by default (backward compatibility)."""
    FastAPICache.init(InMemoryBackend())
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/endpoint")
    @cache(expire=60)
    async def endpoint() -> dict[str, int]:
        call_count["count"] += 1
        if call_count["count"] == 1:
            return {"value": call_count["count"]}
        raise HTTPException(status_code=500, detail="Error")
    
    with TestClient(app) as client:
        # First request - 200
        response1 = client.get("/endpoint")
        assert response1.status_code == 200
        assert response1.headers.get("X-FastAPI-Cache") == "MISS"
        
        # Second request - should use cache (same 200 response)
        response2 = client.get("/endpoint")
        assert response2.status_code == 200
        assert response2.headers.get("X-FastAPI-Cache") == "HIT"
        assert call_count["count"] == 1  # Only called once


def test_cache_with_empty_status_codes_list(reset_cache: Any) -> None:
    """Test that empty status codes list means no caching."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=[])
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/endpoint")
    @cache(expire=60)
    async def endpoint() -> dict[str, int]:
        call_count["count"] += 1
        return {"value": call_count["count"]}
    
    with TestClient(app) as client:
        # First request
        response1 = client.get("/endpoint")
        assert response1.status_code == 200
        assert response1.json()["value"] == 1
        
        # Second request - should NOT use cache
        response2 = client.get("/endpoint")
        assert response2.status_code == 200
        assert response2.json()["value"] == 2
        assert call_count["count"] == 2


def test_cache_none_status_codes_means_cache_all(reset_cache: Any) -> None:
    """Test that None as cache_status_codes means cache all status codes."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=None)
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/endpoint")
    @cache(expire=60)
    async def endpoint() -> dict[str, int]:
        call_count["count"] += 1
        raise HTTPException(status_code=404, detail="Not found")
    
    with TestClient(app) as client:
        # First request - 404
        response1 = client.get("/endpoint")
        assert response1.status_code == 404
        
        # Second request - should use cache
        response2 = client.get("/endpoint")
        assert response2.status_code == 404
        assert call_count["count"] == 1  # Only called once


def test_cache_status_codes_with_multiple_ranges(reset_cache: Any) -> None:
    """Test caching with multiple status code ranges."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=[*range(200, 300), *range(400, 500)])
    
    app = FastAPI()
    status_to_return = {"status": 200}
    call_count = {"count": 0}
    
    @app.get("/endpoint")
    @cache(expire=60)
    async def endpoint() -> dict[str, int]:
        call_count["count"] += 1
        status = status_to_return["status"]
        if status >= 400:
            raise HTTPException(status_code=status, detail="Client error")
        return {"value": call_count["count"]}
    
    with TestClient(app) as client:
        # Test 200 - should cache
        status_to_return["status"] = 200
        response1 = client.get("/endpoint")
        assert response1.status_code == 200
        assert call_count["count"] == 1
        
        response2 = client.get("/endpoint")
        assert response2.status_code == 200
        assert call_count["count"] == 1  # Used cache
        
        # Test 404 - should cache
        call_count["count"] = 0
        status_to_return["status"] = 404
        response3 = client.get("/endpoint?q=1")  # Different cache key
        assert response3.status_code == 404
        assert call_count["count"] == 1
        
        response4 = client.get("/endpoint?q=1")
        assert response4.status_code == 404
        assert call_count["count"] == 1  # Used cache
        
        # Test 500 - should NOT cache
        call_count["count"] = 0
        status_to_return["status"] = 500
        response5 = client.get("/endpoint?q=2")  # Different cache key
        assert response5.status_code == 500
        assert call_count["count"] == 1
        
        response6 = client.get("/endpoint?q=2")
        assert response6.status_code == 500
        assert call_count["count"] == 2  # Not cached


def test_regular_function_with_status_codes(reset_cache: Any) -> None:
    """Test that regular (non-endpoint) functions ignore status code filtering."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=[200])
    
    call_count = {"count": 0}
    
    @cache(expire=60)
    async def regular_function() -> int:
        call_count["count"] += 1
        return call_count["count"]
    
    # Regular functions don't have response objects, so status codes don't apply
    result1 = pytest.asyncio.run(regular_function())
    assert result1 == 1
    
    result2 = pytest.asyncio.run(regular_function())
    assert result2 == 1  # Should be cached
    assert call_count["count"] == 1


def test_status_code_check_happens_before_caching(reset_cache: Any) -> None:
    """Test that status code is checked before storing in cache."""
    FastAPICache.init(InMemoryBackend(), cache_status_codes=[200])
    
    app = FastAPI()
    call_count = {"count": 0}
    
    @app.get("/flaky")
    @cache(expire=60)
    async def flaky_endpoint() -> dict[str, int]:
        call_count["count"] += 1
        if call_count["count"] % 2 == 1:
            raise HTTPException(status_code=500, detail="Odd request fails")
        return {"value": call_count["count"]}
    
    with TestClient(app) as client:
        # First request - 500, should NOT cache
        response1 = client.get("/flaky")
        assert response1.status_code == 500
        assert call_count["count"] == 1
        
        # Second request - 200, should cache
        response2 = client.get("/flaky")
        assert response2.status_code == 200
        assert response2.json()["value"] == 2
        assert call_count["count"] == 2
        
        # Third request - should use cached 200 response
        response3 = client.get("/flaky")
        assert response3.status_code == 200
        assert response3.json()["value"] == 2
        assert call_count["count"] == 2  # Not called again
