# Conditional Caching by HTTP Status Code

## Problem Brief

FastAPI-cache currently caches all responses regardless of HTTP status code. Error responses (4xx, 5xx) are cached alongside successful ones, leading to poor user experience when transient errors are served repeatedly.

Build a feature allowing developers to configure which HTTP status codes should be cached, both globally and per-endpoint. For example, cache only 2xx responses, or cache 2xx and 4xx but not 5xx errors.

## Agent Instructions

### Requirements

1. **Global Configuration**: Add `cache_status_codes` parameter to `FastAPICache.init()` accepting an iterable of status codes (e.g., `[200, 201]` or `range(200, 300)`).

2. **Per-Endpoint Override**: Add `cache_status_codes` parameter to `@cache()` decorator that overrides global configuration.

3. **Backward Compatibility**: When `cache_status_codes` is `None` (default), cache all status codes maintaining current behavior.

4. **Status Code Check**: Before storing a response, check if `response.status_code` is in the allowed list. Only cache if it matches.

5. **Non-endpoint Functions**: Regular functions (not HTTP endpoints) ignore status code filtering since there's no Response object.

### Implementation Steps

- Add `_cache_status_codes` class variable to `FastAPICache`
- Update `FastAPICache.init()` to accept and store `cache_status_codes`
- Add `get_cache_status_codes()` getter method
- Update `FastAPICache.reset()` to clear status codes
- Add `cache_status_codes` parameter to `@cache()` decorator
- Implement status code check before `backend.set()`
- Ensure per-endpoint config overrides global config

### Acceptance Criteria

- `./test.sh base` passes (existing tests still work)
- `./test.sh new` passes (new feature tests pass)
- Caching respects configured status codes
- Default behavior unchanged (backward compatible)

## Test Assumptions

**File Path**: `tests/test_status_code_caching.py`

**Modified Files**:
- `fastapi_cache/__init__.py`: Add `cache_status_codes` parameter and storage
- `fastapi_cache/decorator.py`: Add status code checking logic
