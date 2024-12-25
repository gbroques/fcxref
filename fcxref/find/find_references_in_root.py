import logging
from pathlib import Path
from re import Pattern
from typing import List
from xml.etree.ElementTree import Element

from .match import Match
from .query import Query
from .reference import Reference
from .xml_property import XMLProperty
from .xml_property_name import XMLPropertyName

__all__ = ['find_references_in_root']

logger = logging.getLogger(__name__)

def find_references_in_root(document_path: str,
                            root: Element,
                            query: Query) -> List[Reference]:
    references = []
    xpath_template = "ObjectData/Object[@name='{}']/Properties/Property[@name='{}']"

    object_data = root.find('ObjectData')
    for object in object_data.findall('Object'):
        properties_element = object.find('Properties')
        object_name = object.attrib['name']
        logger.debug(f"Checking ObjectData/Object[@name='{object_name}']")

        for property_element in properties_element.findall('Property'):
            property_element_name = property_element.attrib['name']
            property_xpath = xpath_template.format(
                object_name, property_element_name)
            matches = find_matches(document_path, property_element, query)
            for match in matches:
                xpath = property_xpath + '/' + match.location_xpath
                reference = Reference(document_path,
                              object_name,
                              property_element_name,
                              match.reference_attribute,
                              match.location,
                              match.matched_text,
                              match.content,
                              xpath)
                logger.debug(f'Found {repr(reference)}')
                references.append(reference)
    return references


def find_matches(document_path: str,
                 property_element: Element,
                 query: Query) -> List[Match]:
    property_element_name = property_element.attrib['name']
    if does_property_have_potential_references(property_element_name):
        logger.debug(f"Checking   Properties/Property[@name='{property_element_name}']")
        xml_property = create_xml_property(document_path, property_element, query)
        return xml_property.find_matches()
    else:
        return []


def create_xml_property(document_path, property_element: Element, query) -> XMLProperty:
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
    document = Path(document_path).stem
    if property_element_name == XMLPropertyName.cells.value:
        return XMLProperty(property_element,
                           nested_element_name='Cells',
                           child_element_name='Cell',
                           reference_attributes=['content', 'alias'],
                           location_attribute='address',
                           pattern=r'\b{}\b'.format(query.property_name) if document == query.document else query.to_regex())
    elif property_element_name == XMLPropertyName.ExpressionEngine.value:
        return XMLProperty(property_element,
                           nested_element_name='ExpressionEngine',
                           child_element_name='Expression',
                           reference_attributes=['expression'],
                           location_attribute='path',
                           pattern=r'\b{}\.{}\b'.format(query.object_name, query.property_name) if document == query.document else query.to_regex())
    return None


def does_property_have_potential_references(property_element_name: str) -> bool:
    return any([p for p in list(XMLPropertyName) if property_element_name == p.value])
