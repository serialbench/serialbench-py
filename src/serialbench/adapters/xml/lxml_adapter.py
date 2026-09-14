from .. import XmlAdapter
from ..base import _module_version


class LxmlAdapter(XmlAdapter):
    name = "lxml"
    capabilities = frozenset({"dom", "parse", "generate", "xpath", "streaming"})

    def version(self):
        return _module_version("lxml")

    def parse(self, data):
        from lxml import etree

        return etree.fromstring(data.encode())

    def generate(self, data) -> str:
        from lxml import etree

        root = data if isinstance(data, etree._Element) else self._to_element("root", data)
        return etree.tostring(root, pretty_print=True, encoding="unicode")

    def xpath_query(self, document, expression) -> int:
        return len(document.xpath(expression))

    def stream_parse(self, data, sink):
        from lxml import etree

        for event, elem in etree.iterparse(io_string(data), events=("start", "end")):
            sink(event, elem.tag)
            elem.clear()

    def _to_element(self, tag, value):
        from lxml import etree

        if isinstance(value, dict):
            elem = etree.Element(tag)
            for k, v in value.items():
                elem.append(self._to_element(k, v))
            return elem
        if isinstance(value, list):
            holder = etree.Element(tag)
            for item in value:
                holder.append(self._to_element("item", item))
            return holder
        elem = etree.Element(tag)
        elem.text = str(value)
        return elem


def io_string(data):
    import io

    return io.BytesIO(data.encode())
