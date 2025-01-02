import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.find import Query, Reference, make_find


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    documents = ['MainDocument', 'ExampleDocument']
    root_by_document_path = {}
    for document in documents:
        document_xml_path = Path(__file__).parent.joinpath(f'{document}.xml')
        with open(document_xml_path) as f:
            document_xml = f.read()
        root_by_document_path[f'{document}.FCStd'] = ElementTree.fromstring(document_xml)
    return root_by_document_path


class FindTest(unittest.TestCase):

    def test_find_with_document_object_and_property(self):
        find = make_find(find_root_by_document_path)
        references = find('base_path',
                          Query('MainDocument', 'Spreadsheet', 'Value'))

        self.assertEqual(len(references), 10)

        xpath0 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='A1']"
        self.assertEqual(references[0],
                         Reference('MainDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'A1',
                                   'Value',
                                   "'Value",
                                   xpath0))
        
        xpath1 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[1],
                         Reference('MainDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'alias',
                                   'B1',
                                   'Value',
                                   'Value',
                                   xpath1))
        
        xpath2 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B2']"
        self.assertEqual(references[2],
                         Reference('MainDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'B2',
                                   'Value',
                                   '=Value',
                                   xpath2))
        
        xpath3 = "ObjectData/Object[@name='Box']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Height']"
        self.assertEqual(references[3],
                         Reference('MainDocument.FCStd',
                                   'Box',
                                   'ExpressionEngine',
                                   'expression',
                                   'Height',
                                   'Value',
                                   'Cylinder.Value',
                                   xpath3))

        xpath4 = "ObjectData/Object[@name='Box']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Length']"
        self.assertEqual(references[4],
                         Reference('MainDocument.FCStd',
                                   'Box',
                                   'ExpressionEngine',
                                   'expression',
                                   'Length',
                                   'Value',
                                   'Spreadsheet.Value',
                                   xpath4))
        
        xpath5 = "ObjectData/Object[@name='Box']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Width']"
        self.assertEqual(references[5],
                         Reference('MainDocument.FCStd',
                                   'Box',
                                   'ExpressionEngine',
                                   'expression',
                                   'Width',
                                   'Value',
                                   '<<Spreadsheet>>.Value',
                                   xpath5))

        xpath6 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[6],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'B1',
                                   'MainDocument#Spreadsheet.Value',
                                   '=MainDocument#Spreadsheet.Value',
                                   xpath6))

        xpath7 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='A1']"
        self.assertEqual(references[7],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'A1',
                                   'Value',
                                   '\'Value',
                                   xpath7))

        xpath8 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[8],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'alias',
                                   'B1',
                                   'Value',
                                   'Value',
                                   xpath8))

        xpath9 = "ObjectData/Object[@name='Box']/Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression[@path='Length']"
        self.assertEqual(references[9],
                         Reference('ExampleDocument.FCStd',
                                   'Box',
                                   'ExpressionEngine',
                                   'expression',
                                   'Length',
                                   'Value',
                                   'Spreadsheet.Value',
                                   xpath9))


    def test_find_with_document_and_object(self):
        find = make_find(find_root_by_document_path)
        references = find('base_path', Query('MainDocument', 'Spreadsheet'))

        self.assertEqual(len(references), 1)

        xpath0 = "ObjectData/Object[@name='Spreadsheet']/Properties/Property[@name='cells']/Cells/Cell[@address='B1']"
        self.assertEqual(references[0],
                         Reference('ExampleDocument.FCStd',
                                   'Spreadsheet',
                                   'cells',
                                   'content',
                                   'B1',
                                   'MainDocument#Spreadsheet',
                                   '=MainDocument#Spreadsheet.Value',
                                   xpath0))


if __name__ == '__main__':
    unittest.main()
