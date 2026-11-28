import time

from .adapters import cbor, html, xml, json, yaml, toml
from .memory import profile_parse

REGISTRY = {"xml": xml.REGISTER, "json": json.REGISTER, "yaml": yaml.REGISTER, "toml": toml.REGISTER, "cbor": cbor.REGISTER, "html": html.REGISTER}

ITERATIONS = {"small": 10, "medium": 3, "large": 1}
WARMUP = 3

def _artifact(name):
    from .test_data import artifact

    return artifact(name)


def _run_xpath(adapter, data):
    # Same queries as the Ruby harness's XPATH_QUERIES — cross-language
    # numbers are only comparable when the workloads match the fixtures.
    doc = adapter.parse(data)
    adapter.xpath_query(doc, "//user | //record")
    adapter.xpath_query(doc, "//user[@id='101']")
    adapter.xpath_query(doc, "//preferences/theme")


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
    # schema/query faces: the adapter resolves its per-shape schema or
    # plan from the document root and compiles it once per stem; the
    # teptris/yeptris/leptris faces parse internally, so raw data is
    # passed (diff parses both sides inside the adapter too).
    "validation": lambda a, data: a.validate(data, None),
    "c14n": lambda a, data: a.c14n(data),
    "diff": lambda a, data: a.diff_walk(data),
    "plan": lambda a, data: a.plan_walk(data),
}


def _selected_adapters(operation, fmt):
    for cls in REGISTRY[fmt]:
        adapter = cls()
        if not adapter.available:
            continue
        if operation == "parsing" and not adapter.supports("parse"):
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
        if operation in ("validation", "c14n", "diff", "plan") and not adapter.supports(operation):
            continue
        yield adapter


def run_format(fmt, test_data, sizes=("small", "medium", "large")) -> dict:
    result = {"parsing": [], "generation": [], "xpath": [], "xquery": [], "xslt": [], "xslt30": [], "validation": [], "c14n": [], "diff": [], "plan": [], "streaming": [], "memory": []}
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
