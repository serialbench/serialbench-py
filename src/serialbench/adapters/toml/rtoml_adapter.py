from .. import TomlAdapter
from ..base import _module_version


class RtomlAdapter(TomlAdapter):
    name = "rtoml"
    capabilities = frozenset({"dom", "parse", "generate", "arrays_of_tables", "inline_tables"})

    def version(self):
        return _module_version("rtoml")

    def parse(self, data):
        import rtoml

        return rtoml.loads(data)

    def generate(self, data) -> str:
        import rtoml

        return rtoml.dumps(data)
