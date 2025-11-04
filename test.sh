#!/bin/bash
set -e

case "$1" in
  base)
    # Run existing test suite; should pass on the base commit
    python3 -m pytest tests/test_codecs.py tests/test_decorator.py
    ;;
  new)
    # Run only the newly added tests; expected to fail before implementing the feature
    python3 -m pytest \
      tests/test_cache_size_limit.py::test_global_max_cache_size \
      tests/test_cache_size_limit.py::test_per_endpoint_max_cache_size \
      tests/test_cache_size_limit.py::test_per_endpoint_overrides_global \
      tests/test_cache_size_limit.py::test_cache_size_limit_logging \
      tests/test_cache_size_limit.py::test_no_size_limit
    ;;
  *)
    echo "Usage: ./test.sh {base|new}"
    exit 1
    ;;
esac
