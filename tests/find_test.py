import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from freecad_external_links.find import Match, Reference, make_find


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
        matches = find('base_path',
                       Reference('Master', 'Spreadsheet', 'Value'))

        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0],
                         Match('Test.FCStd', 'Spreadsheet', 'cells', 'B1'))
        self.assertEqual(matches[1],
                         Match('Test.FCStd', 'Cylinder', 'ExpressionEngine', 'Radius'))


if __name__ == '__main__':
    unittest.main()
