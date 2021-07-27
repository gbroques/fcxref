import re
from typing import Callable, List
from xml.etree.ElementTree import Element

from .property import Property

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

    def find_locations(self, property: Property) -> List[str]:
        find_references = self._make_find_references(property)
        nested_element = self.property_element.find(self.nested_element_name)
        return find_references(nested_element)

    def _make_find_references(self, property: Property) -> Callable[[Element], List[str]]:
        return make_find_references_in_property_element(self.child_element_name,
                                                        self.reference_attribute,
                                                        self.location_attribute,
                                                        property)


def make_find_references_in_property_element(child_element_name: str,
                                             reference_attribute: str,
                                             location_attribute: str,
                                             property: Property) -> Callable[[Element], List[str]]:
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
    def find_references_in_property_element(property_element: Element) -> List[str]:
        locations = []
        for child_element in property_element.findall(child_element_name):
            content = child_element.attrib[reference_attribute]
            pattern = re.compile(str(property))
            match = pattern.search(content)
            if match:
                locations.append(child_element.attrib[location_attribute])
        return locations
    return find_references_in_property_element
