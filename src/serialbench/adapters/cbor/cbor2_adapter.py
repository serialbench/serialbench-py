from .. import CborAdapter
from ..base import _module_version


class Cbor2Adapter(CborAdapter):
    name = "cbor2"
    capabilities = frozenset({"dom", "parse", "generate", "canonical"})

    def _probe(self):
        import cbor2  # noqa: F401

        self.parse(b"\xa1\x65probe\xf5")

    def version(self):
        return _module_version("cbor2")

    def parse(self, data):
        import cbor2

        return cbor2.loads(data)

    def generate(self, data) -> bytes:
        import cbor2

        return cbor2.dumps(data, canonical=True)
