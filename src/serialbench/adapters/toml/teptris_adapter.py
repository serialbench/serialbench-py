from .. import TomlAdapter
from ..base import _module_version


class TeptrisAdapter(TomlAdapter):
    name = "teptris"

    def _probe(self):
        import teptris  # noqa: F401

        self.parse("probe = true\n")

    def version(self):
        return _module_version("teptris")

    def parse(self, data):
        import teptris

        return teptris.loads(data)

    def generate(self, data) -> str:
        import teptris

        return teptris.dumps(data)
