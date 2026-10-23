from .tomllib_adapter import TomllibAdapter
from .tomlkit_adapter import TomlkitAdapter
from .rtoml_adapter import RtomlAdapter
from .tomli_w_adapter import TomliWAdapter
from .teptris_adapter import TeptrisAdapter

REGISTER = [TomllibAdapter, TomlkitAdapter, RtomlAdapter, TomliWAdapter, TeptrisAdapter]
