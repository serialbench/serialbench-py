# tomli-w is write-only by design (stdlib tomllib's write twin).
from .. import TomlAdapter
from ..base import _module_version


class TomliWAdapter(TomlAdapter):
    name = "tomli-w"
    capabilities = frozenset({"dom", "generate"})

    def _probe(self):
        self.generate({"probe": True})

    def version(self):
        return _module_version("tomli_w")

    def generate(self, data) -> str:
        import tomli_w

        return tomli_w.dumps(data)
