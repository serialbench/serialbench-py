from .lxml_html_adapter import LxmlHtmlAdapter
from .leptris_adapter import LeptrisHtmlAdapter
from .leptris_whatwg_adapter import LeptrisWhatwgAdapter

REGISTER = [LxmlHtmlAdapter, LeptrisHtmlAdapter, LeptrisWhatwgAdapter]
