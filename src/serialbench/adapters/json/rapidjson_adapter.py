from .. import JsonAdapter
from ..base import _module_version


class RapidjsonAdapter(JsonAdapter):
    name = "python-rapidjson"

    def version(self):
        return _module_version("rapidjson")

    def parse(self, data):
        import rapidjson

        return rapidjson.loads(data)

    def generate(self, data) -> str:
        import rapidjson

        return rapidjson.dumps(data)
