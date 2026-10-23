from .lxml_html_adapter import LxmlHtmlAdapter
from .selectolax_adapter import SelectolaxAdapter
from .leptris_adapter import LeptrisHtmlAdapter
from .leptris_whatwg_adapter import LeptrisWhatwgAdapter

REGISTER = [LxmlHtmlAdapter, SelectolaxAdapter, LeptrisHtmlAdapter, LeptrisWhatwgAdapter]
