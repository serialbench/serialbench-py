# yeptris-py 0.6.35.2 ships the JSON dump (dumps) — but it mis-encodes
# strings shaped like exponent notation ("1e0" -> 1.0) while the Ruby
# binding is exact, so :generate stays out of the capability set until
# dumps round-trips the canonical fixtures (yeptris-py#141).
from .. import JsonAdapter
from ..base import _module_version


class YeptrisJsonAdapter(JsonAdapter):
    name = "yeptris-json"
    capabilities = frozenset({"dom", "parse"})

    def _probe(self):
        self.parse('{"probe":true}')

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris.json

        return yeptris.json.loads(data)
