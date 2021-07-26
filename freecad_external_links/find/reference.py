__all__ = ['Reference']

# TODO: Rename to Location?
class Reference:
    """Represents a fully-qualified location of a property."""

    def __init__(self,
                 document: str,
                 object_name: str,
                 property_name: str) -> None:
        self.document = document
        self.object_name = object_name
        self.property_name = property_name

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        return '{}#{}.{}'.format(self.document, self.object_name, self.property_name)
