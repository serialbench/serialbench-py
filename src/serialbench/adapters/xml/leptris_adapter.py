import io

from .. import XmlAdapter


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
        {"dom", "parse", "generate", "xpath", "streaming", "xquery", "xslt", "xslt30"}
    )

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

    def stream_parse(self, data, sink):
        import io

        for _event, elem in _leptris().iterparse(io.StringIO(data)):
            sink("element", elem.tag)
