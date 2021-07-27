import re
from typing import Callable, List
from xml.etree.ElementTree import Element

from .reference import Reference

__all__ = ['XMLProperty']


class XMLProperty:
    """Represents a property in the XML with a potential cross-document reference."""

    def __init__(self,
                 property_element: Element,
                 nested_element_name: str,
                 child_element_name: str,
                 reference_attribute: str,
                 location_attribute: str) -> None:
        self.property_element = property_element
        self.nested_element_name = nested_element_name
        self.child_element_name = child_element_name
        self.reference_attribute = reference_attribute
        self.location_attribute = location_attribute

    def find_locations(self, reference: Reference) -> List[str]:
        find_references = self._make_find_references(reference)
        nested_element = self.property_element.find(self.nested_element_name)
        return find_references(nested_element)

    def _make_find_references(self, reference: Reference) -> Callable[[Element], List[str]]:
        return make_find_references_in_property(self.child_element_name,
                                                self.reference_attribute,
                                                self.location_attribute,
                                                reference)


def make_find_references_in_property(child_element_name: str,
                                     reference_attribute: str,
                                     location_attribute: str,
                                     reference: Reference) -> Callable[[Element], List[str]]:
    """
    XML Examples::

       <Cell address="B1" content="=Main#Spreadsheet.Value" alias="Value1" />
       <Expression path="Radius" expression="Main#Spreadsheet.Value"/>

    +--------------------+---------------------+--------------------+
    | child_element_name | reference_attribute | location_attribute |
    +====================+=====================+====================+
    | Cell               | content             | address            |
    +--------------------+---------------------+--------------------+
    | Expression         | expression          | path               |
    +--------------------+---------------------+--------------------+
    """
    def find_references_in_property(property: Element) -> List[str]:
        locations = []
        for child_element in property.findall(child_element_name):
            content = child_element.attrib[reference_attribute]
            pattern = re.compile(str(reference))
            match = pattern.search(content)
            if match:
                locations.append(child_element.attrib[location_attribute])
        return locations
    return find_references_in_property
