# Response Size Limit for Caching

## Problem Brief

Add the ability to prevent caching of responses that exceed a configurable size threshold. This feature helps prevent memory/storage issues from caching unexpectedly large responses. The implementation should support both global configuration and per-endpoint overrides, with automatic logging when responses are skipped due to size constraints.

## Agent Instructions

### Requirements

1. **Add `max_cache_size` parameter to `FastAPICache.init()`** in `fastapi_cache/__init__.py`:
   - Add class variable `_max_cache_size: ClassVar[Optional[int]] = None`
   - Add parameter `max_cache_size: Optional[int] = None` to `init()` method
   - Add getter method `get_max_cache_size() -> Optional[int]`
   - Update `reset()` to clear `_max_cache_size`

2. **Add `max_cache_size` parameter to `@cache()` decorator** in `fastapi_cache/decorator.py`:
   - Add `max_cache_size: Optional[int] = None` parameter to decorator
   - Add to nonlocal variables in inner function
   - Retrieve global value if per-endpoint value is None

3. **Implement size checking** in decorator's cache miss path:
   - After encoding with `coder.encode()`, check `len(to_cache)`
   - If size exceeds limit, skip `backend.set()` call
   - Log info message when skipping (must include "size" and "skip")
   - Return response normally to client

4. **Configuration priority**: Per-endpoint `max_cache_size` overrides global setting

### Acceptance Criteria

- Base tests pass: `./test.sh base`
- New tests pass: `./test.sh new`
- Global size limit prevents caching large responses
- Per-endpoint limit works independently and overrides global
- Size limit violations logged at INFO level
- No size limit means all responses cache normally

## Test Assumptions

**New test file**: `tests/test_cache_size_limit.py`

**New signatures**:
- `FastAPICache.init(..., max_cache_size: Optional[int] = None)`
- `FastAPICache.get_max_cache_size() -> Optional[int]`
- `@cache(..., max_cache_size: Optional[int] = None)`

**Logging**: Log message at INFO level containing "size" and "skip" when skipping cache.
