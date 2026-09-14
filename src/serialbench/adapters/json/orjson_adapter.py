from .. import JsonAdapter
from ..base import _module_version


class OrjsonAdapter(JsonAdapter):
    name = "orjson"
    capabilities = frozenset({"dom", "parse", "generate", "pretty_print"})

    def version(self):
        return _module_version("orjson")

    def parse(self, data):
        import orjson

        return orjson.loads(data)

    def generate(self, data) -> str:
        import orjson

        return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode()
