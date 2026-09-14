from .base import Adapter

XML_FEATURE_KEYS = ("xpath", "streaming")
JSON_FEATURE_KEYS = ("pretty_print", "streaming", "symbol_keys")
YAML_FEATURE_KEYS = ("streaming",)
TOML_FEATURE_KEYS = ("comments", "arrays_of_tables", "inline_tables")


def _features(adapter, keys):
    return {k: adapter.supports(k) for k in keys}


class XmlAdapter(Adapter):
    format = "xml"
    capabilities = frozenset({"dom", "parse", "generate"})

    def features(self):
        base = {k: self.supports(k) for k in ("xpath", "streaming", "stax")}
        base["namespaces"] = True
        base["validation"] = False
        return base


class JsonAdapter(Adapter):
    format = "json"
    capabilities = frozenset({"dom", "parse", "generate", "pretty_print"})

    def features(self):
        return _features(self, JSON_FEATURE_KEYS)


class YamlAdapter(Adapter):
    format = "yaml"
    capabilities = frozenset({"dom", "parse", "generate"})

    def features(self):
        return _features(self, YAML_FEATURE_KEYS)


class TomlAdapter(Adapter):
    format = "toml"
    capabilities = frozenset({"dom", "parse", "generate", "arrays_of_tables", "inline_tables", "multiline_strings"})

    def features(self):
        return _features(self, TOML_FEATURE_KEYS)
