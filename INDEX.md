# Problem Set Index - Response Size Limit for Caching

## Quick Start

**Read this first:** `PROBLEM.md` (269 words)
**Usage guide:** `README_PROBLEM_SET.md`

## Core Deliverables (Required)

| File | Purpose | Size |
|------|---------|------|
| **test.sh** | Test runner with `base` and `new` modes | 711 B |
| **tests/test_cache_size_limit.py** | New test suite (5 tests) | 5.9 KB |
| **test.patch** | Git diff of test files only | 7.1 KB |
| **solution.patch** | Git diff of implementation only | 4.4 KB |
| **PROBLEM.md** | Problem description & instructions | 2.1 KB |

## Supporting Documentation

| File | Purpose |
|------|---------|
| **README_PROBLEM_SET.md** | Complete usage instructions |
| **SUMMARY.md** | Problem set overview |
| **INDEX.md** | This file - navigation guide |
| **PROBLEM_SET_COMPLETE.txt** | Completion checklist |

## Patch Contents

### test.patch
- `test.sh` - New file
- `tests/test_cache_size_limit.py` - New file

### solution.patch  
- `fastapi_cache/__init__.py` - Modified
- `fastapi_cache/decorator.py` - Modified

## Test Commands

```bash
# Run base tests (existing test suite)
./test.sh base

# Run new tests (feature tests)
./test.sh new

# Run all tests
./test.sh base && ./test.sh new
```

## Quick Reference

### Usage Pattern 1: Problem Solver
1. Read `PROBLEM.md`
2. `git apply test.patch`
3. `./test.sh base` (should pass)
4. `./test.sh new` (should fail)
5. Implement feature
6. `./test.sh base && ./test.sh new` (both should pass)

### Usage Pattern 2: Reviewer
1. `git apply test.patch`
2. `git apply solution.patch`
3. `./test.sh base && ./test.sh new`
4. Review implementation

## Feature API

### Global Configuration
```python
FastAPICache.init(
    backend=InMemoryBackend(),
    max_cache_size=1024  # bytes
)
```

### Per-Endpoint Configuration
```python
@app.get("/endpoint")
@cache(expire=60, max_cache_size=512)  # bytes
async def my_endpoint():
    return {"data": "..."}
```

## Implementation Summary

**Files Modified:** 2
- `fastapi_cache/__init__.py` - Added global `max_cache_size` configuration
- `fastapi_cache/decorator.py` - Added size checking and logging

**Lines Changed:** ~40 lines
**New Tests:** 5 comprehensive tests
**Documentation:** 269 words (under 300 limit)

## Validation Checklist

✅ All required files created
✅ test.patch contains only test files
✅ solution.patch contains only implementation files
✅ PROBLEM.md under 300 words
✅ test.sh follows specified format
✅ No existing PR found for this feature
✅ All patches are git-compatible
✅ Tests follow project conventions

---

**Status:** ✅ Complete and ready for delivery
**Date:** 2025-11-04
**Branch:** cursor/implement-response-size-limit-for-caching-3110
