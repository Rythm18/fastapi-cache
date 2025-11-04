# Response Size Limit for Caching - Problem Set

This is a complete problem set for implementing a response size limit feature in fastapi-cache2.

## Deliverables

1. **test.sh** - Test runner script with `base` and `new` modes
2. **tests/test_cache_size_limit.py** - Comprehensive test suite (5 tests)
3. **test.patch** - Git patch with test files (test.sh + new tests)
4. **solution.patch** - Git patch with implementation (FastAPICache + decorator changes)
5. **PROBLEM.md** - Problem description and build instructions (269 words)
6. **SUMMARY.md** - Overview of the problem set

## Usage

### For Problem Solvers (Agent/Developer)

1. **Read the problem**: Start with `PROBLEM.md`
2. **Apply tests**: `git apply test.patch`
3. **Verify base tests pass**: `./test.sh base`
4. **Verify new tests fail**: `./test.sh new` (expected to fail)
5. **Implement the feature** according to requirements in `PROBLEM.md`
6. **Verify all tests pass**: `./test.sh base && ./test.sh new`

### For Reviewers

1. **Apply tests**: `git apply test.patch`
2. **Apply solution**: `git apply solution.patch`
3. **Run all tests**: `./test.sh base && ./test.sh new`
4. **Review implementation** in `fastapi_cache/__init__.py` and `fastapi_cache/decorator.py`

## Feature Summary

Adds `max_cache_size` parameter to:
- `FastAPICache.init()` - Global size limit
- `@cache()` decorator - Per-endpoint size limit (overrides global)

When a response exceeds the size limit, it's not cached and an INFO log is written.

## Test Coverage

- ✅ Global size limit enforcement
- ✅ Per-endpoint size limit enforcement
- ✅ Per-endpoint overrides global setting
- ✅ Logging when cache is skipped
- ✅ Unlimited caching when no limit is set

## Files Modified by solution.patch

- `fastapi_cache/__init__.py` - Added `max_cache_size` parameter and storage
- `fastapi_cache/decorator.py` - Added size checking logic

## Notes

- Problem description is under 300 words (269 words)
- All patches are git-compatible
- Tests follow existing project conventions
- Implementation includes proper logging and error handling
- No existing PR found for this feature in the repository
