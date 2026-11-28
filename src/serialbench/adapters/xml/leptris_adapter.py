import io

from .. import XmlAdapter

# Per-shape descriptor specs (compile once per stem, mirroring the
# ruby/C faces). Dialect: a NESTED row applies its child plan to each
# match, so a wrapper element (records -> record) needs its own
# intermediate plan whose rows bind the repeated children.
_XML_PLANS = {
    "config": {
        "element_name": "config",
        "children": [
            {"name": "database", "kind": "nested", "plan": {
                "element_name": "database",
                "children": [
                    {"name": "host", "kind": "scalar"},
                    {"name": "port", "kind": "scalar"},
                    {"name": "name", "kind": "scalar"},
                    {"name": "user", "kind": "scalar"},
                    {"name": "password", "kind": "scalar"},
                ],
            }},
            {"name": "cache", "kind": "nested", "plan": {
                "element_name": "cache",
                "children": [
                    {"name": "enabled", "kind": "scalar"},
                    {"name": "ttl", "kind": "scalar"},
                ],
            }},
        ],
    },
    "users": {
        "element_name": "users",
        "children": [
            {"name": "user", "kind": "nested", "plan": {
                "element_name": "user",
                "attributes": {"id": {"kind": "scalar"}},
                "children": [
                    {"name": "name", "kind": "scalar"},
                    {"name": "email", "kind": "scalar"},
                    {"name": "created_at", "kind": "scalar"},
                    {"name": "profile", "kind": "nested", "plan": {
                        "element_name": "profile",
                        "children": [
                            {"name": "age", "kind": "scalar"},
                            {"name": "city", "kind": "scalar"},
                            {"name": "preferences", "kind": "nested", "plan": {
                                "element_name": "preferences",
                                "children": [
                                    {"name": "theme", "kind": "scalar"},
                                    {"name": "notifications", "kind": "scalar"},
                                ],
                            }},
                        ],
                    }},
                ],
            }},
        ],
    },
    "dataset": {
        "element_name": "dataset",
        "children": [
            {"name": "header", "kind": "nested", "plan": {
                "element_name": "header",
                "children": [
                    {"name": "created", "kind": "scalar"},
                    {"name": "count", "kind": "scalar"},
                    {"name": "format", "kind": "scalar"},
                ],
            }},
            {"name": "records", "kind": "nested", "plan": {
                "element_name": "records",
                "children": [
                    {"name": "record", "kind": "nested", "plan": {
                        "element_name": "record",
                        "attributes": {"id": {"kind": "scalar"}},
                        "children": [
                            {"name": "timestamp", "kind": "scalar"},
                            {"name": "data", "kind": "nested", "plan": {
                                "element_name": "data",
                                "children": [
                                    {"name": "field1", "kind": "scalar"},
                                    {"name": "field2", "kind": "scalar"},
                                    {"name": "field3", "kind": "scalar"},
                                ],
                            }},
                            {"name": "metadata", "kind": "nested", "plan": {
                                "element_name": "metadata",
                                "children": [
                                    {"name": "source", "kind": "scalar"},
                                    {"name": "version", "kind": "scalar"},
                                    {"name": "checksum", "kind": "scalar"},
                                ],
                            }},
                        ],
                    }},
                ],
            }},
        ],
    },
}


def _leptris():
    import leptris

    return leptris


class LeptrisAdapter(XmlAdapter):
    name = "leptris"
    # The Sep 2026 windows gate (native ops off on win32) is gone: the
    # gate-era wheel shipped no engine DLL at all — the crash was an
    # environment artifact, and leptris-py#306 found no repro on any
    # Windows path (wheels are MSVC-built; the engine is vendored since
    # 1.9.278). Windows is covered by the test matrix again.
    capabilities = frozenset(
        {
            "dom",
            "parse",
            "generate",
            "xpath",
            "streaming",
            "xquery",
            "xslt",
            "xslt30",
            "c14n",
            "diff",
            "plan",
        }
    )

    def __init__(self):
        self._plans = {}

    def _probe(self):
        _leptris().fromstring("<probe/>")

    def version(self):
        try:
            return _leptris().libleptris_version()
        except Exception:  # noqa: BLE001
            return "unknown"

    def parse(self, data):
        return _leptris().fromstring(data)

    def generate(self, data) -> str:
        return _leptris().tostring(data).decode()

    def xpath_query(self, document, expression) -> int:
        result = document.xpath(expression)
        return len(result) if isinstance(result, (list, tuple)) else 1

    def stream_parse(self, data, sink):
        for _event, elem in _leptris().iterparse(io.StringIO(data)):
            sink("element", elem.tag)

    def xquery_eval(self, document, expression) -> int:
        result = _leptris().XQuery(expression)(document)
        return len(result) if isinstance(result, (list, tuple)) else 1

    def xslt_transform(self, document, stylesheet) -> str:
        out = _leptris().XSLT(stylesheet)(document)
        text = _leptris().tostring(out)
        return text.decode() if isinstance(text, bytes) else text

    def c14n(self, data) -> bytes:
        from leptris.document import Document

        return _leptris().c14n(Document.parse(data))

    def diff_walk(self, data) -> int:
        from leptris import xmldiff
        from leptris.document import Document

        diff = xmldiff.diff(
            Document.parse(data), Document.parse(data), ignore_ws_text=True
        )
        return len(diff)

    # plan.materialize is the fused parse + walk + free hot path;
    # the descriptor follows the document root (config/users/dataset)
    def plan_walk(self, data) -> dict:
        from leptris.plan import Plan

        stem = self._stem(data)
        plan = self._plans.get(stem)
        if plan is None:
            plan = self._plans[stem] = Plan(_XML_PLANS[stem])
        return plan.materialize(data)

    def _stem(self, data) -> str:
        if "<users" in data:
            return "users"
        if "<dataset" in data:
            return "dataset"
        return "config"
