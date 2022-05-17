from typing import Optional

__all__ = ['Query']


class Query:
    """Represents a query to find cross-document references to.

    May be a query to find references to:
    
    1. an object
    2. or property of an object.

    Which you can form in a FreeCAD expression.

    See `Expressions: Cross-document linking <https://wiki.freecadweb.org/Expressions#Cross-document_linking>`_.
    """

    def __init__(self,
                 document: str,
                 object_name: str,
                 property_name: Optional[str] = None) -> None:
        self.document = document
        self.object_name = object_name
        self.property_name = property_name

    def to_regex(self):
        regex = self.document + '#' + self.object_name
        if self.property_name:
            regex += '\.' + self.property_name
        return regex

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        string = self.document + '#' + self.object_name
        if self.property_name:
            string += '.' + self.property_name
        return string
