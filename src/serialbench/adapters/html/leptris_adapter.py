from .. import HtmlAdapter
from ..base import _module_version


class LeptrisHtmlAdapter(HtmlAdapter):
    """html4 mode: the libxml2/lxml-parity engine (upstream default)."""

    name = "leptris"
    capabilities = frozenset({"dom", "parse", "xpath"})

    def _probe(self):
        import leptris.html

        leptris.html.fromstring("<p>probe</p>")

    def version(self):
        return _module_version("leptris")

    def parse(self, data):
        import leptris.html

        return leptris.html.fromstring(data)

    def xpath_query(self, document, expression):
        result = document.xpath(expression)
        return result if isinstance(result, int) else len(result)
