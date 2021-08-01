from re import Pattern
from typing import Callable, List
from xml.etree.ElementTree import Element

from .match import Match

__all__ = ['XMLProperty']


class XMLProperty:
    """Represents a property in the XML with a potential cross-document reference.

    Encapsulates the logic for finding a reference to a property.
    """

    def __init__(self,
                 property_element: Element,
                 nested_element_name: str,
                 child_element_name: str,
                 reference_attributes: List[str],
                 location_attribute: str) -> None:
        self.property_element = property_element
        self.nested_element_name = nested_element_name
        self.child_element_name = child_element_name
        self.reference_attributes = reference_attributes
        self.location_attribute = location_attribute

    def find_matches(self, pattern: Pattern) -> List[Match]:
        find_references = self._make_find_references()
        nested_element = self.property_element.find(self.nested_element_name)
        return find_references(nested_element, pattern)

    def _make_find_references(self) -> Callable[[Element, Pattern], List[Match]]:
        return make_find_references_in_property_element(self.child_element_name,
                                                        self.reference_attributes,
                                                        self.location_attribute)


def make_find_references_in_property_element(child_element_name: str,
                                             reference_attributes: List[str],
                                             location_attribute: str) -> Callable[[Element, Pattern], List[Match]]:
    """
    XML Examples::

       <Cell address="B1" content="=Main#Spreadsheet.Value" alias="Value" />
       <Expression path="Radius" expression="Main#Spreadsheet.Value" />

    +--------------------+----------------------+--------------------+
    | child_element_name | reference_attributes | location_attribute |
    +====================+======================+====================+
    | Cell               | [content]            | address            |
    +--------------------+----------------------+--------------------+
    | Expression         | [expression]         | path               |
    +--------------------+----------------------+--------------------+
    """
    def find_references_in_property_element(property_element: Element, property_pattern: Pattern) -> List[Match]:
        matches = []
        for child_element in property_element.findall(child_element_name):
            for reference_attribute in reference_attributes:
                if reference_attribute in child_element.attrib:
                    content = child_element.attrib[reference_attribute]
                    match = property_pattern.search(content)
                    if match:
                        matched_text = match.group(0)
                        location_xpath = "{}/{}[@{}='{}']".format(
                            property_element.tag,
                            child_element.tag,
                            location_attribute,
                            child_element.attrib[location_attribute]
                        )
                        matches.append(
                            Match(reference_attribute,
                                  child_element.attrib[location_attribute],
                                  matched_text,
                                  location_xpath))
        return matches
    return find_references_in_property_element
