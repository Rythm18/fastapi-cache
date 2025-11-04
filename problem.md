# Conditional Caching by HTTP Status Code

## Problem Brief

FastAPI-cache currently caches all responses regardless of status code, meaning errors (4xx, 5xx) are cached alongside successful responses. Add support for filtering which status codes should be cached.

## Agent Instructions

Add a `cache_status_codes` parameter that accepts an iterable of HTTP status codes (e.g., `[200, 201]` or `range(200, 300)`). This should work at two levels:

1. **Global configuration** via `FastAPICache.init(cache_status_codes=...)`
2. **Per-endpoint override** via `@cache(cache_status_codes=...)`

Before storing a response in cache, check if its status code is in the allowed set. If not, skip caching but return the response normally. Per-endpoint configuration should override global settings.

For regular functions (non-HTTP endpoints), status code filtering doesn't apply since there's no Response object.

### Acceptance Criteria

- Existing tests pass (`./test.sh base`)
- New feature tests pass (`./test.sh new`)
- Backward compatible: `None` (default) caches all status codes
- Empty list `[]` caches nothing

## Test Assumptions

- Parameter must be named `cache_status_codes` (not `allowed_status_codes` or similar)
- `None` means cache all status codes (not "cache nothing")
- Tests expect modifications to `fastapi_cache/__init__.py` and `fastapi_cache/decorator.py`
