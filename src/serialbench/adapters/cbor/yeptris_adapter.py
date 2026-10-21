# yeptris-py grew a CBOR face (yeptris.cbor) in 0.6.x: load/dump over the
# same FFI document. Full parse + generate as of 0.6.35.1, which fixes dump
# fidelity (yeptris-ruby#293 — exponent-notation strings encoded as floats).
from .. import CborAdapter
from ..base import _module_version


class YeptrisCborAdapter(CborAdapter):
    name = "yeptris-cbor"
    capabilities = frozenset({"dom", "parse", "generate"})

    def _probe(self):
        self.parse(b"\xf5")

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris.cbor

        return yeptris.cbor.load(data)

    def generate(self, data) -> bytes:
        import yeptris.cbor

        return yeptris.cbor.dump(data)
