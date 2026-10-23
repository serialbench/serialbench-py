from .. import JsonAdapter
from ..base import _module_version


class UjsonAdapter(JsonAdapter):
    name = "ujson"
    capabilities = frozenset({"dom", "parse", "generate", "pretty_print"})

    def version(self):
        return _module_version("ujson")

    def parse(self, data):
        import ujson

        return ujson.loads(data)

    def generate(self, data) -> str:
        import ujson

        return ujson.dumps(data, indent=2)
