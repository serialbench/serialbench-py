from .. import YamlAdapter
from ..base import _module_version

# Per-shape plan specs (compile once per stem, mirroring the js wasm
# face): the canonical yaml keys are symbol-style, so wire names and
# path segments carry the leading colon.
_YAML_PLANS = {
    "config": (
        '{"kind":"map","path":[":config",":database"],"children":['
        '{"name":":host","kind":"str"},{"name":":port","kind":"int"},'
        '{"name":":name","kind":"str"},{"name":":user","kind":"str"},'
        '{"name":":password","kind":"str"}]}'
    ),
    "users": (
        '{"kind":"seq","path":[":users"],"children":['
        '{"name":":id","kind":"int"},{"name":":name","kind":"str"},'
        '{"name":":email","kind":"str"},{"name":":created_at","kind":"str"}]}'
    ),
    "dataset": (
        '{"kind":"map","path":[":dataset",":records"],"children":['
        '{"name":":id","kind":"int"},{"name":":timestamp","kind":"str"}]}'
    ),
}


class YeptrisYamlAdapter(YamlAdapter):
    name = "yeptris-yaml"
    capabilities = frozenset({"dom", "parse", "generate", "streaming", "plan"})

    def __init__(self):
        self._plans = {}

    def _probe(self):
        import yeptris  # noqa: F401

        self.parse("probe: true")

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris

        return yeptris.load(data)

    def generate(self, data) -> str:
        import yeptris

        return yeptris.dump(data)

    def stream_parse(self, data, sink):
        import yeptris

        for doc in yeptris.load_all(data):
            sink("document", doc)

    def plan_walk(self, data):
        # plan.walk parses the document itself; the per-shape spec
        # follows the root key (config/users/dataset)
        import yeptris.plan

        stem = self._stem(data)
        plan = self._plans.get(stem)
        if plan is None:
            plan = self._plans[stem] = yeptris.plan.compile_plan(_YAML_PLANS[stem])
        return plan.walk(data).to_rows()

    def _stem(self, data) -> str:
        if ":users" in data:
            return "users"
        if ":dataset" in data:
            return "dataset"
        return "config"
