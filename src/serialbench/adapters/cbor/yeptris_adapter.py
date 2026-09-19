# yeptris-py 0.6.7.x exposes YAML only - no CBOR API yet. This adapter is a
# placeholder that stays unavailable (and says why) until upstream ships one.
from .. import CborAdapter


class YeptrisCborAdapter(CborAdapter):
    name = "yeptris-cbor"
    capabilities = frozenset()

    def _probe(self):
        raise ImportError("yeptris-py has no CBOR API yet (YAML only)")

    def version(self):
        return "unknown"
