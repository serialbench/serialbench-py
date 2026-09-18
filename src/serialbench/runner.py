import time

from .adapters import xml, json, yaml, toml
from .memory import profile_parse

REGISTRY = {"xml": xml.REGISTER, "json": json.REGISTER, "yaml": yaml.REGISTER, "toml": toml.REGISTER}

ITERATIONS = {"small": 10, "medium": 3, "large": 1}
WARMUP = 3

def _artifact(name):
    from .test_data import artifact

    return artifact(name)


def _run_xpath(adapter, data):
    doc = adapter.parse(data)
    adapter.xpath_query(doc, "//book")
    adapter.xpath_query(doc, "//book[@id='101']")
    adapter.xpath_query(doc, "//book[price > 30]/title")


OPERATIONS = {
    "parsing": lambda a, data: a.parse(data),
    "generation": lambda a, data: a.generate(a.parse(data)),
    "xpath": _run_xpath,
    "xquery": lambda a, data: (
        a.xquery_eval(a.parse(data), "count(//user | //record)"),
        a.xquery_eval(a.parse(data), "//record[@id='101']/data/field1"),
    ),
    "xslt": lambda a, data: a.xslt_transform(a.parse(data), _artifact("transform.xsl")),
    "xslt30": lambda a, data: a.xslt_transform(a.parse(data), _artifact("transform30.xsl")),
    "streaming": lambda a, data: a.stream_parse(data, lambda event, payload: None),
}


def _selected_adapters(operation, fmt):
    for cls in REGISTRY[fmt]:
        adapter = cls()
        if not adapter.available:
            continue
        if operation == "generation" and not adapter.supports("generate"):
            continue
        if operation == "xpath" and not adapter.supports("xpath"):
            continue
        if operation == "xquery" and not adapter.supports("xquery"):
            continue
        if operation in ("xslt", "xslt30") and not adapter.supports("xslt30"):
            continue
        if operation == "streaming" and not (adapter.supports("streaming") or adapter.supports("sax")):
            continue
        yield adapter


def run_format(fmt, test_data, sizes=("small", "medium", "large")) -> dict:
    result = {"parsing": [], "generation": [], "xpath": [], "xquery": [], "xslt": [], "xslt30": [], "validation": [], "streaming": [], "memory": []}
    for operation, handler in list(OPERATIONS.items()) + [("memory", None)]:
        for size in sizes:
            data = test_data[size][fmt]
            for adapter in _selected_adapters(operation, fmt):
                try:
                    if operation == "memory":
                        row = _memory_row(adapter, fmt, size, data)
                    else:
                        row = _timed_row(adapter, fmt, size, data, operation, handler)
                    if row:
                        result[operation].append(row)
                except Exception as exc:  # noqa: BLE001 - one adapter must not kill the leg
                    print(f"    {fmt}/{adapter.name}: ERROR - {exc}")
    return result


def _timed_row(adapter, fmt, size, data, operation, handler):
    iterations = ITERATIONS[size]
    for _ in range(WARMUP):
        handler(adapter, data)
    start = time.perf_counter()
    for _ in range(iterations):
        handler(adapter, data)
    elapsed = time.perf_counter() - start
    return {
        "adapter": adapter.name,
        "format": fmt,
        "data_size": size,
        "time_per_iterations": elapsed,
        "time_per_iteration": elapsed / iterations,
        "iterations_per_second": iterations / elapsed,
        "iterations_count": iterations,
    }


def _memory_row(adapter, fmt, size, data):
    if not adapter.available:
        return None
    stats = profile_parse(adapter, data, size)
    return {
        "adapter": adapter.name,
        "format": fmt,
        "data_size": size,
        **stats,
    }
