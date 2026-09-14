from .. import YamlAdapter
from ..base import _module_version


class YeptrisYamlAdapter(YamlAdapter):
    name = "yeptris-yaml"
    capabilities = frozenset({"dom", "parse", "generate", "streaming"})

    def _probe(self):
        import yeptris  # noqa: F401

        self.parse("probe: true")

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris

        return yeptris.load(data)

    def generate(self, data) -> str:
        import yeptris

        return yeptris.dump(data)

    def stream_parse(self, data, sink):
        import yeptris

        for doc in yeptris.load_all(data):
            sink("document", doc)
