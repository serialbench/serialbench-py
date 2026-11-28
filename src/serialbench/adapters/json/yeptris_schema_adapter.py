from .. import JsonAdapter
from serialbench.test_data import fixtures_dir


def _stem(data: str) -> str:
    if '"users"' in data:
        return "users"
    if '"dataset"' in data:
        return "dataset"
    return "config"


class YeptrisSchemaAdapter(JsonAdapter):
    # Validation face: one compiled JSON Schema per canonical shape
    # (yeptris-py's compiled-schema economy), then validate per
    # iteration.
    name = "yeptris-schema"
    capabilities = frozenset({"validation"})

    def __init__(self):
        self._schemas = {}

    def _probe(self):
        from yeptris._validate import Schema

        Schema('{"type":"object"}')

    def version(self):
        try:
            import yeptris

            return getattr(yeptris, "__version__", "unknown")
        except Exception:  # noqa: BLE001
            return "unknown"

    def features(self):
        return {"validation": True}

    def validate(self, data, _schema=None) -> bool:
        from yeptris._validate import Schema

        stem = _stem(data)
        schema = self._schemas.get(stem)
        if schema is None:
            path = fixtures_dir() / f"{stem}.schema.json"
            schema = self._schemas[stem] = Schema(path.read_text())
        return schema.is_valid(data)
