import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.rename import make_rename


def find_root_by_document_path(base_path: str, document_pattern: str = '*') -> Dict[str, Element]:
    document = 'MasterDocument.xml' if document_pattern == 'Master' else 'Document.xml'
    filepath = 'Master.FCStd' if document_pattern == 'Master' else 'Test.FCStd'
    return {
        filepath: load_root(document)
    }


def load_root(document_xml_path: str) -> Element:
    path = Path(__file__).parent.joinpath(document_xml_path)
    with open(path) as f:
        document_xml = f.read()
    return ElementTree.fromstring(document_xml)


class RenameTest(unittest.TestCase):

    def test_rename(self):
        rename = make_rename(find_root_by_document_path)

        root_by_document_path = rename('base_path',
                                       'Master',
                                       'Spreadsheet',
                                       ('Value', 'RenamedValue'))

        self.assertEqual(len(root_by_document_path.items()), 2)

        self.assertIn('Test.FCStd', root_by_document_path)
        document_root = root_by_document_path['Test.FCStd']
        expected_document_root = load_root('RenamedDocument.xml')
        self.assertEqual(ElementTree.tostring(document_root),
                         ElementTree.tostring(expected_document_root))

        self.assertIn('Master.FCStd', root_by_document_path)
        master_root = root_by_document_path['Master.FCStd']
        expected_master_root = load_root('RenamedMasterDocument.xml')
        self.assertEqual(ElementTree.tostring(master_root),
                         ElementTree.tostring(expected_master_root))


if __name__ == '__main__':
    unittest.main()
