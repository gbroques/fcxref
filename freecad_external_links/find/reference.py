__all__ = ['Reference']


class Reference:
    """Represents a reference to a property in another document."""

    def __init__(self,
                 document: str,
                 object_name: str,
                 property_name: str,
                 location: str) -> None:
        self.document = document
        self.object_name = object_name
        self.property_name = property_name
        self.location = location

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        return '{} {}.{} ({})'.format(
            self.document,
            self.object_name,
            self.location,
            self.property_name)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Reference):
            return (
                self.document == o.document and
                self.object_name == o.object_name and
                self.property_name == o.property_name and
                self.location == o.location
            )
        return False
