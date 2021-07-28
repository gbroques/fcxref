__all__ = ['Property']


class Property:
    """Represents a fully-qualified property of an object in a document.

    Which you can reference in a FreeCAD expression.

    See `Expressions: Cross-document linking <https://wiki.freecadweb.org/Expressions#Cross-document_linking>`_.
    """

    def __init__(self,
                 document: str,
                 object_name: str,
                 property_name: str) -> None:
        self.document = document
        self.object_name = object_name
        self.property_name = property_name

    def to_regex(self):
        return '{}#{}\.{}'.format(
            self.document,
            self.object_name,
            self.property_name)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        return '{}#{}.{}'.format(
            self.document,
            self.object_name,
            self.property_name)
