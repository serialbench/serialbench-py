from .. import TomlAdapter
from ..base import _module_version


class TomllibAdapter(TomlAdapter):
    name = "tomllib"

    # stdlib tomllib (and its tomli backport) are parse-only.
    capabilities = frozenset({"dom", "parse", "arrays_of_tables", "inline_tables"})

    def _probe(self):
        self.parse("probe = true\n")

    def version(self):
        try:
            import tomllib

            return f"stdlib/{tomllib.__name__}"
        except ImportError:
            return _module_version("tomli")

    def parse(self, data):
        try:
            import tomllib

            return tomllib.loads(data)
        except ImportError:
            import tomli

            return tomli.loads(data)
