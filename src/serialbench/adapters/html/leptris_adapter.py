from .. import HtmlAdapter
from ..base import _module_version


class LeptrisHtmlAdapter(HtmlAdapter):
    """html4 mode: the libxml2/lxml-parity engine (upstream default)."""

    name = "leptris"
    # generate() landed in leptris-py 1.9.381.1 (upstream #311); on older
    # wheels the html leg's generation rows fail and autoheal refills the
    # format after the next wheel lands.
    capabilities = frozenset({"dom", "parse", "xpath", "generate"})

    def _probe(self):
        import leptris.html

        leptris.html.fromstring("<p>probe</p>")

    def version(self):
        return _module_version("leptris")

    def parse(self, data):
        import leptris.html

        return leptris.html.fromstring(data)

    def generate(self, document) -> str:
        import leptris.html

        return leptris.html.generate(document)

    def xpath_query(self, document, expression):
        result = document.xpath(expression)
        return result if isinstance(result, int) else len(result)
