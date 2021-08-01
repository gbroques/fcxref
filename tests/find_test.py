import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.find import Property, Reference, make_find


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    document_xml_path = Path(__file__).parent.joinpath('Document.xml')
    with open(document_xml_path) as f:
        document_xml = f.read()
    return {
        'Test.FCStd': ElementTree.fromstring(document_xml)
    }


class FindTest(unittest.TestCase):

    def test_find(self):
        find = make_find(find_root_by_document_path)
        references = find('base_path',
                          Property('Master', 'Spreadsheet', 'Value'))

        self.assertEqual(len(references), 2)

        xpath0 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='A2']"
        self.assertEqual(references[0],
                         Reference('Test.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'A2',
                                   'Master#Spreadsheet.Value',
                                   xpath0))

        xpath1 = "ObjectData/Object[@name='Cylinder']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Radius']"
        self.assertEqual(references[1],
                         Reference('Test.FCStd',
                                   'Cylinder',
                                   'ExpressionEngine',
                                   'expression',
                                   'Radius',
                                   'Master#Spreadsheet.Value',
                                   xpath1))


if __name__ == '__main__':
    unittest.main()
