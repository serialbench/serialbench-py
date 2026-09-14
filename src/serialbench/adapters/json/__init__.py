from .stdlib import StdlibJsonAdapter
from .orjson_adapter import OrjsonAdapter
from .rapidjson_adapter import RapidjsonAdapter
from .yeptris_adapter import YeptrisJsonAdapter  # noqa: F401 (unavailable placeholder)

REGISTER = [StdlibJsonAdapter, OrjsonAdapter, RapidjsonAdapter, YeptrisJsonAdapter]
