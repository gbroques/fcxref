import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.remove import make_remove


def make_find_root_by_document_path(document_name: str):
    def find_root_by_document_path(base_path: str, document_pattern: str = '*') -> Dict[str, Element]:
        document = document_name if document_pattern == '*' else document_pattern
        filepath = '{}.FCStd'.format(document)
        return {
            filepath: load_root('{}.xml'.format(document))
        }
    return find_root_by_document_path


def load_root(document_xml_path: str) -> Element:
    path = Path(__file__).parent.joinpath(document_xml_path)
    with open(path) as f:
        document_xml = f.read()
    return ElementTree.fromstring(document_xml)


class RemoveTest(unittest.TestCase):

    def test_remove(self):
        find_root_by_document_path = make_find_root_by_document_path(
            'ExampleDocument')
        remove = make_remove(find_root_by_document_path)
        root_by_document_path = remove('base_path', 'MainDocument')

        self.assertEqual(len(root_by_document_path.items()), 1)

        self.assertIn('ExampleDocument.FCStd', root_by_document_path)
        example_root = root_by_document_path['ExampleDocument.FCStd']
        expected_document_root = load_root('ExampleDocumentWithoutXLink.xml')
        self.assertMultiLineEqual(ElementTree.tostring(example_root).decode('utf-8'),
                                  ElementTree.tostring(expected_document_root).decode('utf-8'))

    def test_remove_with_multi_xlink(self):
        find_root_by_document_path = make_find_root_by_document_path(
            'ExampleDocumentWithMultiXLink')
        remove = make_remove(find_root_by_document_path)
        root_by_document_path = remove('base_path', 'MainDocument')

        self.assertEqual(len(root_by_document_path.items()), 1)

        self.assertIn('ExampleDocumentWithMultiXLink.FCStd',
                      root_by_document_path)
        example_root = root_by_document_path['ExampleDocumentWithMultiXLink.FCStd']
        expected_document_root = load_root(
            'ExampleDocumentWithoutMultiXLink.xml')
        self.assertMultiLineEqual(ElementTree.tostring(example_root).decode('utf-8'),
                                  ElementTree.tostring(expected_document_root).decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
