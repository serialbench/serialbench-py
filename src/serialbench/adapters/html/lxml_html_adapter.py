from .. import HtmlAdapter
from ..base import _module_version


class LxmlHtmlAdapter(HtmlAdapter):
    name = "lxml-html"
    capabilities = frozenset({"dom", "parse", "generate", "xpath"})

    def _probe(self):
        from lxml import html as lxml_html

        lxml_html.fromstring("<p>probe</p>")

    def version(self):
        return _module_version("lxml")

    def parse(self, data):
        from lxml import html as lxml_html

        return lxml_html.fromstring(data)

    def generate(self, data) -> str:
        from lxml import html as lxml_html

        return lxml_html.tostring(data).decode()

    def xpath_query(self, document, expression):
        return document.xpath(expression)
