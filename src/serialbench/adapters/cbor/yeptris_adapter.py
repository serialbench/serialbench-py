# yeptris-py grew a CBOR face (yeptris.cbor) in 0.6.x: load/dump over the
# same FFI document. Parse-only — dump mis-encodes strings shaped like
# exponent notation ("1e0" -> 1.0), the same codec defect as the Ruby binding.
from .. import CborAdapter
from ..base import _module_version


class YeptrisCborAdapter(CborAdapter):
    name = "yeptris-cbor"
    capabilities = frozenset({"dom", "parse"})

    def _probe(self):
        self.parse(b"\xf5")

    def version(self):
        return _module_version("yeptris")

    def parse(self, data):
        import yeptris.cbor

        return yeptris.cbor.load(data)
