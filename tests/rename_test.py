import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.rename import make_rename_property


def find_root_by_document_path(base_path: str, document_pattern: str = '*') -> Dict[str, Element]:
    document = 'ExampleDocument' if document_pattern == '*' else document_pattern
    filepath = '{}.FCStd'.format(document)
    return {
        filepath: load_root('{}.xml'.format(document))
    }


def load_root(document_xml_path: str) -> Element:
    path = Path(__file__).parent.joinpath(document_xml_path)
    with open(path) as f:
        document_xml = f.read()
    return ElementTree.fromstring(document_xml)


class RenameTest(unittest.TestCase):

    def test_rename_property(self):
        rename_property = make_rename_property(find_root_by_document_path)

        root_by_document_path = rename_property('base_path',
                                                'MainDocument',
                                                'Spreadsheet',
                                                ('Value', 'RenamedValue'))

        self.assertEqual(len(root_by_document_path.items()), 2)

        self.assertIn('ExampleDocument.FCStd', root_by_document_path)
        document_root = root_by_document_path['ExampleDocument.FCStd']
        expected_document_root = load_root('RenamedExampleDocument.xml')
        self.assertMultiLineEqual(ElementTree.tostring(document_root).decode('utf-8'),
                                  ElementTree.tostring(expected_document_root).decode('utf-8'))

        self.assertIn('MainDocument.FCStd', root_by_document_path)
        main_root = root_by_document_path['MainDocument.FCStd']
        expected_main_root = load_root('RenamedMainDocument.xml')
        self.assertMultiLineEqual(ElementTree.tostring(main_root).decode('utf-8'),
                                  ElementTree.tostring(expected_main_root).decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
