# selectolax (lexbor backend) is a read-only HTML tokenizer/DOM — parse-only.
from .. import HtmlAdapter
from ..base import _module_version


class SelectolaxAdapter(HtmlAdapter):
    name = "selectolax"
    capabilities = frozenset({"dom", "parse"})

    def _probe(self):
        self.parse("<p>probe</p>")

    def version(self):
        return _module_version("selectolax")

    def parse(self, data):
        # lexbor backend: the default modest engine is deprecated (and its
        # import errors on 1.0+); lexbor is the actively developed backend.
        from selectolax.lexbor import LexborHTMLParser

        return LexborHTMLParser(data)
