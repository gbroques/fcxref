from copy import deepcopy
from typing import Callable, Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .remove_document_from_xlinks import remove_document_from_multi_xlinks

__all__ = ['make_remove']


def make_remove(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def remove(base_path: str, document_name: str) -> Dict[str, Element]:
        """
        The below are example Doument.xml snippets of no XLinks and XLinks.

        EMPTY
        -----
        <Cells Count="2" xlink="1">
            <XLinks count="0">
            </XLinks>
            <Cell address="A1" content="Test" />
            <Cell address="B1" content="5" alias="Test" />
        </Cells>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            <ExpressionEngine count="0">
            </ExpressionEngine>
        </Property>

        XLINKS
        ------
        <Cells Count="4" xlink="1">
            <XLinks count="1" docs="1">
                <DocMap name="Master" label="Master" index="0"/>
                <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
            </XLinks>
            <Cell address="A1" content="Value" />
            <Cell address="B1" content="=Master#Spreadsheet.Value" alias="Value1" />
            <Cell address="D8" content="Value" />
            <Cell address="E8" content="=&lt;&lt;Master&gt;&gt;#&lt;&lt;Spreadsheet&gt;&gt;.Value" alias="Value2" />
        </Cells>
        <ExpressionEngine count="2" xlink="1">
            <XLinks count="2" docs="2">
                <DocMap name="Master" label="Master" index="1"/>
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
                <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
            </XLinks>
            <Expression path="Height" expression="Cube#Box.Height"/>
            <Expression path="Radius" expression="Master#Spreadsheet.Value"/>
        </ExpressionEngine>

        FreeCAD Source:
        * `Cells <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/PropertySheet.cpp#L277-L304>`_
        * `Expression Engine <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyExpressionEngine.cpp#L163-L185>`_
        * `XLinks <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyLinks.cpp#L4473-L4510>`_
        * `XLink <https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyLinks.cpp#L3155-L3249>`_
        """
        root_by_document_path = find_root_by_document_path(base_path)

        renamed_root_by_document_path = {}
        for document_path, root in root_by_document_path.items():
            copy = deepcopy(root)
            xlinks_parent_elements = copy.findall('.//XLinks/..')
            for xlinks_parent_element in xlinks_parent_elements:
                for xlinks_element in xlinks_parent_element.findall('XLinks'):
                    doc_map_xpath = f"./DocMap[@name='{document_name}']"
                    matching_doc_map_elements = xlinks_element.findall(
                        doc_map_xpath)
                    if len(matching_doc_map_elements):
                        xlinks_count = int(xlinks_element.attrib['count'])
                        if xlinks_count == 1:
                            if xlinks_parent_element.tag == 'Cells':
                                xlinks_element.attrib['count'] = '0'
                                del xlinks_element.attrib['docs']
                                for child in list(xlinks_element):
                                    xlinks_element.remove(child)
                            elif xlinks_parent_element.tag == 'ExpressionEngine':
                                del xlinks_parent_element.attrib['xlink']
                                xlinks_parent_element.remove(xlinks_element)
                        else:
                            updated_xlinks_element = remove_document_from_multi_xlinks(
                                xlinks_element, document_name)
                            xlinks_parent_element.remove(xlinks_element)
                            xlinks_parent_element.insert(
                                0, updated_xlinks_element)
            if ElementTree.tostring(copy) != ElementTree.tostring(root):
                renamed_root_by_document_path[document_path] = copy

        return renamed_root_by_document_path
    return remove
