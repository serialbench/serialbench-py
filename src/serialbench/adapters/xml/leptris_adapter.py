from .. import XmlAdapter


def _leptris():
    import leptris

    return leptris


class LeptrisAdapter(XmlAdapter):
    name = "leptris"
    # no :streaming yet - leptris-py iterparse on large documents errors and
    # then leaves the library in a state where subsequent calls hang
    # (upstream issue); re-add when fixed.
    capabilities = frozenset({"dom", "parse", "generate", "xpath"})

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
        import io

        for _event, elem in _leptris().iterparse(io.StringIO(data)):
            sink("element", elem.tag)
