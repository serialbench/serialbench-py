import importlib
import warnings


class Adapter:
    name = "abstract"
    format = None
    capabilities = frozenset()

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    _available = None

    @property
    def available(self) -> bool:
        if self._available is None:
            try:
                self._probe()
                self._available = True
            except Exception as exc:  # noqa: BLE001 - probe must never crash the run
                warnings.warn(f"{self.name} unavailable: {exc.__class__.__name__}: {exc}")
                self._available = False
        return self._available

    def _probe(self):
        self.parse(self.probe_document())

    def probe_document(self) -> str:
        return {"xml": "<probe/>", "json": '{"probe":true}', "yaml": "probe: true", "toml": "probe = true\n"}[self.format]

    def version(self) -> str:
        return "unknown"

    def features(self) -> dict:
        return {}

    # --- protocol ---
    def parse(self, data: str):
        raise NotImplementedError

    def generate(self, data) -> str:
        raise NotImplementedError


def _module_version(module_name: str, attr: str = "__version__") -> str:
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, attr, "unknown")
    except Exception:  # noqa: BLE001
        return "unknown"
