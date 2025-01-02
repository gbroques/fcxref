from .extract_document import extract_document

__all__ = ['Reference']

class Reference:
    """Represents a reference to a property or object in another document."""

    def __init__(self,
                 document_path: str,
                 object_name: str,
                 property_name: str,
                 reference_attribute: str,
                 location: str,
                 match: str,
                 content: str,
                 xpath: str) -> None:
        self.document_path = document_path
        self.object_name = object_name
        self.property_name = property_name
        self.reference_attribute = reference_attribute
        self.location = location
        self.match = match
        self.content = content
        self.xpath = xpath

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return (
            f'Reference(document_path="{self.document_path}",\n' +
            f'          object_name="{self.object_name}",\n' +
            f'          property_name="{self.property_name}",\n' +
            f'          reference_attribute="{self.reference_attribute}",\n' +
            f'          location="{self.location}",\n' +
            f'          match="{self.match}",\n' +
            f'          content="{self.content}",\n' +
            f'          xpath="{self.xpath}")'
        )

    def _to_string(self):
        return '{} {}.{} {}'.format(
            extract_document(self.document_path),
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
                self.content == o.content and
                self.xpath == o.xpath
            )
        return False
