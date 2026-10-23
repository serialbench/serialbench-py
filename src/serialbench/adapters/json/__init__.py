from .stdlib import StdlibJsonAdapter
from .orjson_adapter import OrjsonAdapter
from .msgspec_adapter import MsgspecAdapter
from .ujson_adapter import UjsonAdapter
from .rapidjson_adapter import RapidjsonAdapter
from .yeptris_adapter import YeptrisJsonAdapter  # noqa: F401

REGISTER = [StdlibJsonAdapter, OrjsonAdapter, MsgspecAdapter, UjsonAdapter, RapidjsonAdapter, YeptrisJsonAdapter]
