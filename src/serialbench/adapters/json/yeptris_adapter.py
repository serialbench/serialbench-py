# yeptris-py JSON face: loads + dumps. Dump fidelity shipped in
# 0.6.36.1 (yeptris-py#141 — before that, strings shaped like exponent
# notation encoded as numbers).
from .. import JsonAdapter
from ..base import _module_version


class YeptrisJsonAdapter(JsonAdapter):
    name = "yeptris-json"
    capabilities = frozenset({"dom", "parse", "generate"})

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
