from .. import YamlAdapter
from ..base import _module_version


class RuamelAdapter(YamlAdapter):
    name = "ruamel-yaml"
    capabilities = frozenset({"dom", "parse", "generate"})

    def version(self):
        return _module_version("ruamel.yaml")

    def parse(self, data):
        from ruamel.yaml import YAML

        return YAML(typ="safe", pure=True).load(data)

    def generate(self, data) -> str:
        from io import StringIO

        from ruamel.yaml import YAML

        yaml = YAML(typ="safe", pure=True)
        yaml.default_flow_style = False
        buf = StringIO()
        yaml.dump(data, buf)
        return buf.getvalue()
