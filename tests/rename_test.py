import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.find import Property
from fcxref.rename import make_rename


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    return {
        'Test.FCStd': load_root('Document.xml')
    }


def load_root(document_xml_path: str) -> Element:
    path = Path(__file__).parent.joinpath(document_xml_path)
    with open(path) as f:
        document_xml = f.read()
    return ElementTree.fromstring(document_xml)


class RenameTest(unittest.TestCase):

    def test_rename(self):
        rename = make_rename(find_root_by_document_path)
        from_property = Property('Master', 'Spreadsheet', 'Value')
        to_property = Property('Master', 'Spreadsheet', 'RenamedValue')
        root_by_document_path = rename('base_path',
                                       from_property,
                                       to_property)

        self.assertIn('Test.FCStd', root_by_document_path)
        root = root_by_document_path['Test.FCStd']
        ElementTree.tostring(root)
        expected_root = load_root('RenamedDocument.xml')
        self.assertEqual(ElementTree.tostring(root),
                         ElementTree.tostring(expected_root))


if __name__ == '__main__':
    unittest.main()
