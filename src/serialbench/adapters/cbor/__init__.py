from .cbor2_adapter import Cbor2Adapter
from .yeptris_adapter import YeptrisCborAdapter  # noqa: F401 (unavailable placeholder)

REGISTER = [Cbor2Adapter, YeptrisCborAdapter]
