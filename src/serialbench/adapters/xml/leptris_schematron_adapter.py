from .. import XmlAdapter
from serialbench.test_data import fixtures_dir

_PROBE_SCH = (
    '<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">'
    '<sch:pattern><sch:rule context="/">'
    '<sch:assert test="true()">ok</sch:assert>'
    "</sch:rule></sch:pattern></sch:schema>"
)


def _stem(data: str) -> str:
    if "<users" in data:
        return "users"
    if "<dataset" in data:
        return "dataset"
    return "config"


class LeptrisSchematronAdapter(XmlAdapter):
    # Validation face: one compiled Schematron per canonical shape,
    # then parse+validate per iteration.
    name = "leptris-schematron"
    capabilities = frozenset({"validation"})

    def __init__(self):
        self._schemas = {}

    def _probe(self):
        from leptris.schematron import Schematron

        Schematron(_PROBE_SCH)

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
        from leptris.schematron import Schematron

        stem = _stem(data)
        schema = self._schemas.get(stem)
        if schema is None:
            path = fixtures_dir() / f"{stem}.sch"
            schema = self._schemas[stem] = Schematron(path.read_text())
        return schema.is_valid(Document.parse(data))
