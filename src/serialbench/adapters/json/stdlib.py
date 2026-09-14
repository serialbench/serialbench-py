import json

from .. import JsonAdapter


class StdlibJsonAdapter(JsonAdapter):
    name = "json"

    def version(self):
        return "stdlib"

    def parse(self, data):
        return json.loads(data)

    def generate(self, data) -> str:
        return json.dumps(data)
