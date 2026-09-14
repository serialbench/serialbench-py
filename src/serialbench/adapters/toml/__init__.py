from .tomllib_adapter import TomllibAdapter
from .tomlkit_adapter import TomlkitAdapter
from .teptris_adapter import TeptrisAdapter

REGISTER = [TomllibAdapter, TomlkitAdapter, TeptrisAdapter]
