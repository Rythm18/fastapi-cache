# Problem Set: Conditional Caching by HTTP Status Code

## Overview
This problem set implements a feature for fastapi-cache that allows conditional caching based on HTTP response status codes. The difficulty is estimated at 2-4 hours for an experienced software engineer.

## Deliverables Created

### 1. `test.sh` (executable)
Bash script with two commands:
- `./test.sh base` - Runs existing test suite (should pass on base commit)
- `./test.sh new` - Runs only new feature tests (fails before implementation, passes after)

### 2. `tests/test_status_code_caching.py`
Comprehensive test suite with 10 test cases covering:
- Caching only 2xx status codes
- Caching specific status codes (lists and ranges)
- Per-endpoint override of global configuration
- Backward compatibility (default caches all)
- Empty status code list behavior
- Multiple status code ranges
- Regular function caching (non-HTTP endpoints)
- Status code check timing

### 3. `test.patch`
Git diff containing:
- `test.sh` (new file)
- `tests/test_status_code_caching.py` (new file)
- **Only test files, no implementation**

### 4. Implementation Files (Modified)
- `fastapi_cache/__init__.py` - Added `cache_status_codes` parameter, storage, and getter
- `fastapi_cache/decorator.py` - Added status code checking before caching

### 5. `solution.patch`
Git diff containing:
- Changes to `fastapi_cache/__init__.py`
- Changes to `fastapi_cache/decorator.py`
- **Only implementation, no test files**

### 6. `problem.md`
Problem documentation (268 words, under 300 word limit) with:
- Problem Brief - Plain language description
- Agent Instructions - High-level build plan and acceptance criteria
- Test Assumptions - File paths and modifications expected

## Feature Description

### What It Does
Allows developers to specify which HTTP status codes should be cached:
```python
# Global: only cache 2xx responses
FastAPICache.init(backend, cache_status_codes=range(200, 300))

# Per-endpoint: override to also cache 404s
@app.get("/item")
@cache(expire=60, cache_status_codes=[200, 404])
async def get_item():
    ...
```

### Key Behaviors
- **Default (None)**: Caches all status codes (backward compatible)
- **Empty list []**: Caches nothing
- **Per-endpoint override**: Decorator parameter overrides global setting
- **Regular functions**: Status code filtering doesn't apply (no Response object)

## How to Use This Problem Set

### For Testing (Before Implementation)
```bash
# Existing tests should pass
./test.sh base

# New tests should fail (feature not implemented)
./test.sh new
```

### Applying the Solution
```bash
# Apply test patch first
git apply test.patch

# Verify tests fail
./test.sh new

# Apply solution patch
git apply solution.patch

# Verify tests now pass
./test.sh new
./test.sh base
```

## Files Structure
```
/workspace/
├── test.sh                              # Test runner script
├── test.patch                           # Patch with tests only
├── solution.patch                       # Patch with implementation only
├── problem.md                           # Problem documentation
├── tests/
│   └── test_status_code_caching.py     # New test file
└── fastapi_cache/
    ├── __init__.py                      # Modified (in solution.patch)
    └── decorator.py                     # Modified (in solution.patch)
```

## Verification Checklist

✅ test.sh exists and is executable
✅ test.patch contains only test.sh and test_status_code_caching.py
✅ solution.patch contains only __init__.py and decorator.py changes
✅ problem.md is under 300 words (268 words)
✅ Tests are comprehensive (10 test cases)
✅ Implementation maintains backward compatibility
✅ Per-endpoint override works correctly
✅ No existing tests are broken

## Notes

- The feature has been verified to not conflict with any open PRs in the upstream repository (long2ice/fastapi-cache)
- All patches use standard git diff format
- The implementation follows the existing code style and patterns
- Type hints are properly maintained throughout
