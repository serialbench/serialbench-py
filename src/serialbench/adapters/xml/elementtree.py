import xml.etree.ElementTree as ET

from .. import XmlAdapter


class ElementTreeAdapter(XmlAdapter):
    name = "elementtree"

    # stdlib ElementTree supports only a restricted XPath subset - no
    # relational predicates like //book[price > 30] - so no :xpath claim.
    capabilities = frozenset({"dom", "parse", "generate", "streaming"})

    def version(self):
        return "stdlib"

    def parse(self, data):
        return ET.fromstring(data)

    def generate(self, data) -> str:
        root = data if isinstance(data, ET.Element) else self._to_element("root", data)
        ET.indent(root)
        return ET.tostring(root, encoding="unicode")

    def stream_parse(self, data, sink):
        for event, elem in ET.iterparse(io_string(data), events=("start", "end")):
            sink(event, elem.tag)
            elem.clear()

    def _to_element(self, tag, value):
        if isinstance(value, dict):
            elem = ET.Element(tag)
            for k, v in value.items():
                elem.append(self._to_element(k, v))
            return elem
        if isinstance(value, list):
            holder = ET.Element(tag)
            for item in value:
                holder.append(self._to_element("item", item))
            return holder
        return ET.Element(tag, {"value": str(value)})


def io_string(data):
    import io

    return io.StringIO(data)
