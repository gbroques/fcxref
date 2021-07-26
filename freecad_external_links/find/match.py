__all__ = ['Match']

# TODO: Rename to Reference?
class Match:
    """Represents a reference to an external property."""

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
