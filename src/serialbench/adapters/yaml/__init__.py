from .pyyaml_adapter import PyYamlAdapter
from .ruamel_adapter import RuamelAdapter
from .yeptris_adapter import YeptrisYamlAdapter

REGISTER = [PyYamlAdapter, RuamelAdapter, YeptrisYamlAdapter]
