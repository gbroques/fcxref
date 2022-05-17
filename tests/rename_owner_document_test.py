import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.find import Query
from fcxref.rename.rename_owner_document import rename_owner_document


def find_root_by_document_path(base_path: str, document_pattern: str) -> Dict[str, Element]:
    return {
        'MainDocument.FCStd': load_root('MainDocument.xml')
    }


def load_root(document_xml_path: str) -> Element:
    path = Path(__file__).parent.joinpath(document_xml_path)
    with open(path) as f:
        document_xml = f.read()
    return ElementTree.fromstring(document_xml)


class RenameOwnerDocumentTest(unittest.TestCase):

    def test_rename_owner_document_with_document_name_and_object_name(self):
        from_property = Query('MainDocument', 'Spreadsheet', 'Value')
        to_property_name = 'RenamedValue'
        root_by_document_path = rename_owner_document(
            find_root_by_document_path, '.', from_property, to_property_name)

        self.assertIn('MainDocument.FCStd', root_by_document_path)
        root = root_by_document_path['MainDocument.FCStd']
        expected_root = load_root('RenamedMainDocument.xml')
        self.assertEqual(ElementTree.tostring(root),
                         ElementTree.tostring(expected_root))

    def test_rename_owner_document_with_document_label_and_object_label(self):
        from_property = Query('<<MainDocument>>', '<<Spreadsheet>>', 'Value')
        to_property_name = 'RenamedValue'
        root_by_document_path = rename_owner_document(
            find_root_by_document_path, '.', from_property, to_property_name)

        self.assertIn('MainDocument.FCStd', root_by_document_path)
        root = root_by_document_path['MainDocument.FCStd']
        expected_root = load_root('RenamedMainDocument.xml')
        self.assertEqual(ElementTree.tostring(root),
                         ElementTree.tostring(expected_root))

    def test_rename_owner_document_with_document_name_and_object_label(self):
        from_property = Query('MainDocument', '<<Spreadsheet>>', 'Value')
        to_property_name = 'RenamedValue'
        root_by_document_path = rename_owner_document(
            find_root_by_document_path, '.', from_property, to_property_name)

        self.assertIn('MainDocument.FCStd', root_by_document_path)
        root = root_by_document_path['MainDocument.FCStd']
        expected_root = load_root('RenamedMainDocument.xml')
        self.assertEqual(ElementTree.tostring(root),
                         ElementTree.tostring(expected_root))

    def test_rename_owner_document_with_document_label_and_object_name(self):
        from_property = Query('<<MainDocument>>', 'Spreadsheet', 'Value')
        to_property_name = 'RenamedValue'
        root_by_document_path = rename_owner_document(
            find_root_by_document_path, '.', from_property, to_property_name)

        self.assertIn('MainDocument.FCStd', root_by_document_path)
        root = root_by_document_path['MainDocument.FCStd']
        expected_root = load_root('RenamedMainDocument.xml')
        self.assertEqual(ElementTree.tostring(root),
                         ElementTree.tostring(expected_root))


if __name__ == '__main__':
    unittest.main()
