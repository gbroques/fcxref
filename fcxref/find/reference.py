import os

__all__ = ['Reference']


class Reference:
    """Represents a reference to a property in another document."""

    def __init__(self,
                 document_path: str,
                 object_name: str,
                 property_name: str,
                 reference_attribute: str,
                 location: str,
                 match: str,
                 xpath: str) -> None:
        self.document_path = document_path
        self.object_name = object_name
        self.property_name = property_name
        self.reference_attribute = reference_attribute
        self.location = location
        self.match = match
        self.xpath = xpath

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        return '{} {}.{} ({})'.format(
            format_document_path(self.document_path),
            self.object_name,
            self.location,
            self.reference_attribute)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Reference):
            return (
                self.document_path == o.document_path and
                self.object_name == o.object_name and
                self.property_name == o.property_name and
                self.reference_attribute == o.reference_attribute and
                self.location == o.location and
                self.match == o.match and
                self.xpath == o.xpath
            )
        return False


def format_document_path(document_path: str) -> str:
    return os.path.splitext(os.path.basename(document_path))[0]
