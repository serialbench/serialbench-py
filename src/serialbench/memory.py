import tracemalloc

# Python-heap allocations only: C-extension parsers allocate outside the
# traced heap, so memory numbers are per-runtime (time is the cross-runtime
# metric). Counts parse iterations per size like the Ruby harness, but for
# `large` a single parse is profiled - profiling holds references.
_ITERATIONS = {"small": 10, "medium": 10, "large": 1}


def profile_parse(adapter, data, size) -> dict:
    tracemalloc.start()
    try:
        for _ in range(_ITERATIONS.get(size, 1)):
            adapter.parse(data)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return {
        "total_allocated": peak,
        "total_retained": peak,
        "allocated_memory": peak,
        "retained_memory": peak,
        "profile": "python-heap-peak",
    }
