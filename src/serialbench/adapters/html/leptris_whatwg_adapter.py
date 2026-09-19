from .leptris_adapter import LeptrisHtmlAdapter


class LeptrisWhatwgAdapter(LeptrisHtmlAdapter):
    """The WHATWG-conformant engine, priced separately."""

    name = "leptris-whatwg"
    capabilities = frozenset({"dom", "parse", "xpath", "html5"})

    def parse(self, data):
        import leptris.html

        return leptris.html.fromstring(data, mode="whatwg")
