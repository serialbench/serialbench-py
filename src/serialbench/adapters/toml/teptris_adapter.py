from .. import TomlAdapter
from ..base import _module_version
from serialbench.test_data import fixtures_dir

# Per-shape query plans (teptris-py#173) and JSON Schemas
# (serialbench/fixtures#1) — keyed by the document's root key
# (config/users/dataset), compiled once per stem.
_TOML_PLANS = {
    "config": [
        {"name": "config", "rows": [
            {"name": "database", "rows": ["host", "port", "name", "user", "password"]},
            {"name": "cache", "rows": ["enabled", "ttl"]},
        ]},
    ],
    "users": [
        {"name": "users", "rows": ["id", "name", "email", "created_at"]},
    ],
    "dataset": [
        {"name": "dataset", "rows": [
            {"name": "header", "rows": ["created", "count", "format"]},
            {"name": "records", "rows": ["id", "timestamp"]},
        ]},
    ],
}


class TeptrisAdapter(TomlAdapter):
    name = "teptris"
    capabilities = frozenset({"dom", "parse", "generate", "validation", "plan"})

    def __init__(self):
        super().__init__()
        self._schemas = {}
        self._plans = {}

    def _probe(self):
        import teptris  # noqa: F401

        self.parse("probe = true\n")

    def version(self):
        return _module_version("teptris")

    def parse(self, data):
        import teptris

        return teptris.loads(data)

    def generate(self, data) -> str:
        import teptris

        return teptris.dumps(data)

    def validate(self, data, _schema=None):
        # schema_validate parses the TOML itself; the schema is the
        # per-shape fixture resolved from the root key.
        import teptris

        schema = self._schema_for(data)
        return schema.valid(data)

    def plan_walk(self, data):
        import teptris

        plan = self._plan_for(data)
        return teptris.plan_walk(plan, data)

    def _stem(self, data):
        return next(iter(self.parse(data)))

    def _schema_for(self, data):
        import teptris

        stem = self._stem(data)
        schema = self._schemas.get(stem)
        if schema is None:
            path = fixtures_dir() / f"{stem}.schema.json"
            schema = self._schemas[stem] = teptris.compile_schema(path.read_text())
        return schema

    def _plan_for(self, data):
        import teptris

        stem = self._stem(data)
        plan = self._plans.get(stem)
        if plan is None:
            plan = self._plans[stem] = teptris.plan_build(_TOML_PLANS[stem])
        return plan
