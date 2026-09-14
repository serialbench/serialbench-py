from .. import TomlAdapter
from ..base import _module_version


class TomlkitAdapter(TomlAdapter):
    name = "tomlkit"
    capabilities = frozenset({"dom", "parse", "generate", "arrays_of_tables", "inline_tables", "multiline_strings", "comments"})

    def version(self):
        return _module_version("tomlkit")

    def parse(self, data):
        import tomlkit

        return tomlkit.parse(data)

    def generate(self, data) -> str:
        import tomlkit

        return tomlkit.dumps(data)
