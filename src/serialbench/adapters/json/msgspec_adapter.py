from .. import JsonAdapter
from ..base import _module_version


class MsgspecAdapter(JsonAdapter):
    name = "msgspec"
    capabilities = frozenset({"dom", "parse", "generate"})

    def version(self):
        return _module_version("msgspec")

    def parse(self, data):
        import msgspec

        return msgspec.json.decode(data)

    def generate(self, data) -> str:
        import msgspec

        return msgspec.json.encode(data).decode()
