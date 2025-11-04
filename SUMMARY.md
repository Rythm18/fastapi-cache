# Response Size Limit for Caching - Problem Set Summary

This problem set implements a response size limit feature for fastapi-cache2.

## Files Created

### 1. test.sh
Executable test script with two modes:
- `./test.sh base` - Runs existing test suite (test_codecs.py, test_decorator.py)
- `./test.sh new` - Runs new feature tests from test_cache_size_limit.py

### 2. tests/test_cache_size_limit.py
New test file with 5 comprehensive tests:
- `test_global_max_cache_size` - Tests global size limit
- `test_per_endpoint_max_cache_size` - Tests per-endpoint size limit
- `test_per_endpoint_overrides_global` - Tests override behavior
- `test_cache_size_limit_logging` - Tests logging functionality
- `test_no_size_limit` - Tests unlimited caching

### 3. test.patch
Git diff containing:
- New test.sh script
- New tests/test_cache_size_limit.py file

### 4. Implementation Files
Modified files (included in solution.patch):
- `fastapi_cache/__init__.py` - Added max_cache_size parameter to FastAPICache
- `fastapi_cache/decorator.py` - Added size checking logic to @cache decorator

### 5. solution.patch
Git diff containing all implementation changes

### 6. PROBLEM.md
Problem documentation (269 words) with:
- Problem Brief - Plain language description
- Agent Instructions - Build plans and acceptance criteria
- Test Assumptions - Expected signatures and interfaces

## Feature Overview

The implementation adds:
1. Global `max_cache_size` parameter in `FastAPICache.init()`
2. Per-endpoint `max_cache_size` in `@cache()` decorator
3. Automatic size checking before caching
4. INFO-level logging when responses are skipped
5. Per-endpoint configuration overrides global setting

## Testing

Before implementation:
```bash
./test.sh base  # Should pass
./test.sh new   # Should fail
```

After applying solution.patch:
```bash
./test.sh base  # Should pass
./test.sh new   # Should pass
```

## Applying Patches

```bash
# Apply test files
git apply test.patch

# Apply implementation
git apply solution.patch
```
