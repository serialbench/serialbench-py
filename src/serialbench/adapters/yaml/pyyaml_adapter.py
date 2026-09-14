from .. import YamlAdapter
from ..base import _module_version


class PyYamlAdapter(YamlAdapter):
    name = "pyyaml"
    capabilities = frozenset({"dom", "parse", "generate", "streaming"})

    def version(self):
        ver = _module_version("yaml")
        engine = "libyaml" if self._libyaml() else "pure"
        return f"{ver}+{engine}"

    @staticmethod
    def _libyaml() -> bool:
        try:
            from yaml import CSafeLoader

            return True
        except ImportError:
            return False

    def parse(self, data):
        import yaml

        loader = yaml.CSafeLoader if self._libyaml() else yaml.SafeLoader
        return yaml.load(data, Loader=loader)

    def generate(self, data) -> str:
        import yaml

        return yaml.safe_dump(data, sort_keys=False)

    def stream_parse(self, data, sink):
        import yaml

        loader = yaml.CSafeLoader if self._libyaml() else yaml.SafeLoader
        for doc in yaml.load_all(data, Loader=loader):
            sink("document", doc)
