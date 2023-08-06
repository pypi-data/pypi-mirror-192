from . import _version
from .node import XmlNode, XmlBaseNode
from .factory import XmlNodeFactory

__version__ = _version.get_versions()['version']
__all__ = ['XmlBaseNode', 'XmlNode', 'XmlNodeFactory']
