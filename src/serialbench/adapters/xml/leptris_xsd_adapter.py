from .. import XmlAdapter
from serialbench.test_data import fixtures_dir


def _stem(data: str) -> str:
    if "<users" in data:
        return "users"
    if "<dataset" in data:
        return "dataset"
    return "config"


_PROBE_XSD = (
    '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
    '<xs:element name="probe"/></xs:schema>'
)


class LeptrisXsdAdapter(XmlAdapter):
    # Validation face: one compiled XSD per canonical shape
    # (config/users/dataset), then parse+validate per iteration.
    name = "leptris-xsd"
    capabilities = frozenset({"validation"})

    def __init__(self):
        self._schemas = {}

    def _probe(self):
        from leptris.xsd import XSD

        XSD(_PROBE_XSD)

    def version(self):
        try:
            import leptris

            return leptris.libleptris_version()
        except Exception:  # noqa: BLE001
            return "unknown"

    def features(self):
        return {"validation": True}

    def validate(self, data, _schema=None) -> bool:
        from leptris.document import Document
        from leptris.xsd import XSD

        stem = _stem(data)
        schema = self._schemas.get(stem)
        if schema is None:
            path = fixtures_dir() / f"{stem}.xsd"
            schema = self._schemas[stem] = XSD(path.read_text())
        return schema.validate(Document.parse(data))
