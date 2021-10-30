import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.find import Property, Reference, make_find


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    document_xml_path = Path(__file__).parent.joinpath('ExampleDocument.xml')
    with open(document_xml_path) as f:
        document_xml = f.read()
    return {
        'ExampleDocument.FCStd': ElementTree.fromstring(document_xml)
    }


class FindTest(unittest.TestCase):

    def test_find(self):
        find = make_find(find_root_by_document_path)
        references = find('base_path',
                          Property('MainDocument', 'Spreadsheet', 'Value'))

        self.assertEqual(len(references), 4)

        xpath0 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[0],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'B1',
                                   'MainDocument#Spreadsheet.Value',
                                   xpath0))

        xpath1 = "ObjectData/Object[@name='Box']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Length']"
        self.assertEqual(references[1],
                         Reference('ExampleDocument.FCStd',
                                   'Box',
                                   'ExpressionEngine',
                                   'expression',
                                   'Length',
                                   'MainDocument#Spreadsheet.Value',
                                   xpath1))

        xpath2 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='A1']"
        self.assertEqual(references[2],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'A1',
                                   'Value',
                                   xpath2))

        xpath3 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[3],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'alias',
                                   'B1',
                                   'Value',
                                   xpath3))


if __name__ == '__main__':
    unittest.main()
