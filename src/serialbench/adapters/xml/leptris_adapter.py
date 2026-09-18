import io

from .. import XmlAdapter


def _leptris():
    import leptris

    return leptris


class LeptrisAdapter(XmlAdapter):
    name = "leptris"
    # windows: the native ops (xquery/xslt/xslt30/streaming) segfault inside
    # the mingw wheel (upstream issue) - parse/generate/html stay enabled
    import sys as _sys

    _NATIVE_OPS = frozenset({"streaming", "xquery", "xslt", "xslt30"})
    capabilities = frozenset({"dom", "parse", "generate", "xpath"}) | (
        _NATIVE_OPS if _sys.platform != "win32" else frozenset())

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
