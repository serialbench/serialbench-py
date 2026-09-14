# yeptris-py 0.2.x exposes YAML only - no JSON API yet. This adapter is a
# placeholder that stays unavailable (and says why) until upstream ships one.
from .. import JsonAdapter


class YeptrisJsonAdapter(JsonAdapter):
    name = "yeptris-json"
    capabilities = frozenset()

    def _probe(self):
        raise ImportError("yeptris-py has no JSON API yet (YAML only)")

    def version(self):
        return "unknown"
