from re import Pattern
from typing import List
from xml.etree.ElementTree import Element

from .match import Match
from .reference import Reference
from .xml_property import XMLProperty
from .xml_property_name import XMLPropertyName

__all__ = ['find_references_in_root']


def find_references_in_root(document_path: str,
                            root: Element,
                            pattern: Pattern) -> List[Reference]:
    references = []
    xpath_template = "ObjectData/Object[@name='{}']/Properties/Property[@name='{}']"

    object_data = root.find('ObjectData')
    for object in object_data.findall('Object'):
        properties_element = object.find('Properties')
        object_name = object.attrib['name']

        for property_element in properties_element.findall('Property'):
            property_element_name = property_element.attrib['name']
            property_xpath = xpath_template.format(
                object_name, property_element_name)
            matches = find_matches(property_element, pattern)
            for match in matches:
                xpath = property_xpath + '/' + match.location_xpath
                references.append(
                    Reference(document_path,
                              object_name,
                              property_element_name,
                              match.reference_attribute,
                              match.location,
                              match.matched_text,
                              xpath))
    return references


def find_matches(property_element: Element,
                 pattern: Pattern) -> List[Match]:
    property_element_name = property_element.attrib['name']
    if does_property_have_potential_references(property_element_name):
        xml_property = create_xml_property(property_element)
        return xml_property.find_matches(pattern)
    else:
        return []


def create_xml_property(property_element: Element) -> XMLProperty:
    """
    XML Examples::

        <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
            <Cells Count="4" xlink="1">
                <Cell address="B1" content="=Main#Spreadsheet.Value" alias="Value" />
            </Cells>
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            <ExpressionEngine count="2" xlink="1">
                <Expression path="Radius" expression="Main#Spreadsheet.Value" />
            </ExpressionEngine>
        </Property>    

    +--------------------+---------------------+--------------------+----------------------+--------------------+
    | property_name      | nested_element_name | child_element_name | reference_attributes | location_attribute |
    +====================+=====================+====================+======================+====================+
    | cells              | Cells               | Cell               | [content, alias]     | address            |
    +--------------------+---------------------+--------------------+----------------------+--------------------+
    | ExpressionEngine   | ExpressionEngine    | Expression         | [expression]         | path               |
    +--------------------+---------------------+--------------------+----------------------+--------------------+

    FreeCAD Source:
    * `Property <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyContainer.cpp#L221-L310>`_
    * `Cells <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/PropertySheet.cpp#L277-L304>`_
    * `Expression Engine <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyExpressionEngine.cpp#L163-L185>`_
    """
    property_element_name = property_element.attrib['name']
    if property_element_name == XMLPropertyName.cells.value:
        return XMLProperty(property_element,
                           nested_element_name='Cells',
                           child_element_name='Cell',
                           reference_attributes=['content', 'alias'],
                           location_attribute='address')
    elif property_element_name == XMLPropertyName.ExpressionEngine.value:
        return XMLProperty(property_element,
                           nested_element_name='ExpressionEngine',
                           child_element_name='Expression',
                           reference_attributes=['expression'],
                           location_attribute='path')
    return None


def does_property_have_potential_references(property_element_name: str) -> bool:
    return any([p for p in list(XMLPropertyName) if property_element_name == p.value])
