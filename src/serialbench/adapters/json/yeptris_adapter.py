# yeptris-py 0.6.x ships a JSON face (yeptris.json.loads). Parse-only:
# no dump yet — when upstream ships one it should price like the Ruby
# yeptris-json adapter (parse + generate).
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
