import re
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from .match import Match
from .reference import Reference

__all__ = ['make_find']


def make_find(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def find(base_path: str, reference: Reference) -> List[Match]:
        matches = []
        root_by_document_path = find_root_by_document_path(base_path)
        for document_path, root in root_by_document_path.items():
            matches_in_document = find_references_in_root(
                document_path, root, reference)
            matches.extend(matches_in_document)
        return matches
    return find


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


def make_find_references_in_cells(reference: Reference) -> Callable[[Element], List[str]]:
    return make_find_references_in_property('Cell',
                                            'content',
                                            'address',
                                            reference)


def make_find_references_in_expression_engine(reference: Reference) -> Callable[[Element], List[str]]:
    return make_find_references_in_property('Expression',
                                            'expression',
                                            'path',
                                            reference)


def find_references_in_root(document_path: str,
                            root: Element,
                            reference: Reference) -> List[Match]:
    matches = []
    object_data = root.find('ObjectData')
    for object in object_data:
        properties = object.find('Properties')
        object_name = object.attrib['name']

        for property in properties.findall('Property'):
            property_name = property.attrib['name']
            find_locations = make_find_locations(property)
            locations = find_locations(reference)
            for location in locations:
                matches.append(
                    Match(document_path, object_name, property_name, location))
    return matches


class Property:
    """Represents a property with a potential external or cross-document reference."""

    def __init__(self,
                 property_element: Element,
                 nested_element_name: str,
                 make_find_references: Callable[[Reference], Callable[[Element], List[str]]]) -> None:
        self.property_element = property_element
        self.nested_element_name = nested_element_name
        self.make_find_references = make_find_references

    def find_locations(self, reference: Reference) -> List[str]:
        find_references = self.make_find_references(reference)
        nested_element = self.property_element.find(self.nested_element_name)
        return find_references(nested_element)


def make_find_locations(property_element: Element) -> Callable[[Reference], List[str]]:
    def find_locations(reference: Reference) -> List[str]:
        property_name = property_element.attrib['name']
        properties_with_references = {'cells', 'ExpressionEngine'}
        if property_name in properties_with_references:
            property = create_property(property_element)
            return property.find_locations(reference)
        else:
            return []
    return find_locations


def create_property(property_element: Element) -> Property:
    """
    XML Examples::

        <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
            <Cells Count="4" xlink="1">
                ...
            </Cells>
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            <ExpressionEngine count="2" xlink="1">
                ...
            </ExpressionEngine>
        </Property>

    +--------------------+---------------------+
    | property_name      | nested_element_name |
    +====================+=====================+
    | cells              | Cells               |
    +--------------------+---------------------+
    | ExpressionEngine   | ExpressionEngine    |
    +--------------------+---------------------+

    FreeCAD Source:
    * `Property <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyContainer.cpp#L221-L310>`_
    * `Cells <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/PropertySheet.cpp#L277-L304>`_
    * `Expression Engine <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyExpressionEngine.cpp#L163-L185>`_
    """
    property_name = property_element.attrib['name']
    if property_name == 'cells':
        return Property(property_element, 'Cells', make_find_references_in_cells)
    elif property_name == 'ExpressionEngine':
        return Property(property_element, 'ExpressionEngine', make_find_references_in_expression_engine)
    return None
