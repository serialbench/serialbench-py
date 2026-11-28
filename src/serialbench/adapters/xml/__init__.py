from .elementtree import ElementTreeAdapter
from .lxml_adapter import LxmlAdapter
from .leptris_adapter import LeptrisAdapter
from .leptris_xsd_adapter import LeptrisXsdAdapter
from .leptris_schematron_adapter import LeptrisSchematronAdapter

REGISTER = [LxmlAdapter, ElementTreeAdapter, LeptrisAdapter, LeptrisXsdAdapter, LeptrisSchematronAdapter]
