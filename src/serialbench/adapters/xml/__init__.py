from .elementtree import ElementTreeAdapter
from .lxml_adapter import LxmlAdapter
from .leptris_adapter import LeptrisAdapter

REGISTER = [LxmlAdapter, ElementTreeAdapter, LeptrisAdapter]
