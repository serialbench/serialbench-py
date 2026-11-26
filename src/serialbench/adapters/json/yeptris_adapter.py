# yeptris-py JSON face: loads + dumps. Dump fidelity shipped in
# 0.6.36.1 (yeptris-py#141 — before that, strings shaped like exponent
# notation encoded as numbers). The plan face (yeptris-py#192) prices
# the compiled columnar walk.
from .. import JsonAdapter
from ..base import _module_version

_JSON_PLANS = {
    "config": (
        '{"kind":"map","path":["config","database"],"children":['
        '{"name":"host","kind":"str"},{"name":"port","kind":"int"},'
        '{"name":"name","kind":"str"},{"name":"user","kind":"str"},'
        '{"name":"password","kind":"str"}]}'
    ),
    "users": (
        '{"kind":"seq","path":["users"],"children":['
        '{"name":"id","kind":"int"},{"name":"name","kind":"str"},'
        '{"name":"email","kind":"str"},{"name":"created_at","kind":"str"}]}'
    ),
    "dataset": (
        '{"kind":"map","path":["dataset","records"],"children":['
        '{"name":"id","kind":"int"},{"name":"timestamp","kind":"str"}]}'
    ),
}


class YeptrisJsonAdapter(JsonAdapter):
    name = "yeptris-json"
    capabilities = frozenset({"dom", "parse", "generate", "plan"})

    def __init__(self):
        super().__init__()
        self._plans = {}

    def _probe(self):
        self.parse('{"probe":true}')

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris.json

        return yeptris.json.loads(data)

    def generate(self, data) -> str:
        import yeptris.json

        return yeptris.json.dumps(data)

    def plan_walk(self, data):
        # plan.walk parses the document itself; the per-shape spec
        # follows the root key (config/users/dataset).
        import json as _json
        import yeptris.plan

        stem = next(iter(_json.loads(data)))
        plan = self._plans.get(stem)
        if plan is None:
            plan = self._plans[stem] = yeptris.plan.compile_plan(_JSON_PLANS[stem])
        result = plan.walk(data)
        return result.to_rows()
