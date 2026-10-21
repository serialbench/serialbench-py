from .cbor2_adapter import Cbor2Adapter
from .yeptris_adapter import YeptrisCborAdapter  # noqa: F401 (parse-only)

REGISTER = [Cbor2Adapter, YeptrisCborAdapter]
