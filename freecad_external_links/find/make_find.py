from enum import Enum, unique
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from .match import Match
from .property import Property
from .xml_property import XMLProperty

__all__ = ['make_find']


@unique
class XMLPropertyName(Enum):
    """Enumerates XML property names with potential cross-document references.

    XML Examples::

        <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
            ...
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            ...
        </Property>

    See `Core Changes: Link Properties <https://github.com/realthunder/FreeCAD_assembly3/wiki/Core-Changes#link-properties>`_:

        A new class PropertyXLinkContainer is added to support more complex external link usage,
        such as PropertyExpressionEngine and Spreadsheet::PropertySheet.

    """
    cells = 'cells'
    ExpressionEngine = 'ExpressionEngine'


def make_find(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def find(base_path: str, property: Property) -> List[Match]:
        matches = []
        root_by_document_path = find_root_by_document_path(base_path)
        for document_path, root in root_by_document_path.items():
            matches_in_document = find_references_in_root(
                document_path, root, property)
            matches.extend(matches_in_document)
        return matches
    return find


def find_references_in_root(document_path: str,
                            root: Element,
                            property: Property) -> List[Match]:
    matches = []
    object_data = root.find('ObjectData')
    for object in object_data:
        property_elements = object.find('Properties')
        object_name = object.attrib['name']

        for property_element in property_elements.findall('Property'):
            property_name = property_element.attrib['name']
            find_locations = make_find_locations(property_element)
            locations = find_locations(property)
            for location in locations:
                matches.append(
                    Match(document_path, object_name, property_name, location))
    return matches


def make_find_locations(property_element: Element) -> Callable[[Property], List[str]]:
    def find_locations(property: Property) -> List[str]:
        property_name = property_element.attrib['name']
        if does_property_have_potential_references(property_name):
            xml_property = create_xml_property(property_element)
            return xml_property.find_locations(property)
        else:
            return []
    return find_locations


def create_xml_property(property_element: Element) -> XMLProperty:
    """
    XML Examples::

        <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
            <Cells Count="4" xlink="1">
                <Cell address="B1" content="=Main#Spreadsheet.Value" alias="Value1" />
            </Cells>
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            <ExpressionEngine count="2" xlink="1">
                <Expression path="Radius" expression="Main#Spreadsheet.Value"/>
            </ExpressionEngine>
        </Property>    

    +--------------------+---------------------+--------------------+---------------------+--------------------+
    | property_name      | nested_element_name | child_element_name | reference_attribute | location_attribute |
    +====================+=====================+====================+=====================+====================+
    | cells              | Cells               | Cell               | content             | address            |
    +--------------------+---------------------+--------------------+---------------------+--------------------+
    | ExpressionEngine   | ExpressionEngine    | Expression         | expression          | path               |
    +--------------------+---------------------+--------------------+---------------------+--------------------+

    FreeCAD Source:
    * `Property <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyContainer.cpp#L221-L310>`_
    * `Cells <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/PropertySheet.cpp#L277-L304>`_
    * `Expression Engine <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyExpressionEngine.cpp#L163-L185>`_
    """
    property_name = property_element.attrib['name']
    if property_name == XMLPropertyName.cells.value:
        return XMLProperty(property_element,
                           nested_element_name='Cells',
                           child_element_name='Cell',
                           reference_attribute='content',
                           location_attribute='address')
    elif property_name == XMLPropertyName.ExpressionEngine.value:
        return XMLProperty(property_element,
                           nested_element_name='ExpressionEngine',
                           child_element_name='Expression',
                           reference_attribute='expression',
                           location_attribute='path')
    return None


def does_property_have_potential_references(property_name: str) -> bool:
    return any([p for p in list(XMLPropertyName) if property_name == p.value])
