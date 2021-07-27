import unittest
from pathlib import Path
from xml.etree.ElementTree import Element

from freecad_external_links.find_root_by_document_path import \
    find_root_by_document_path


class FindRootByDocumentPath(unittest.TestCase):

    def test_find_root_by_document_path(self):
        tests_path = Path(__file__).parent

        root_by_document_path = find_root_by_document_path(str(tests_path))

        self.assertEqual(len(root_by_document_path.items()), 1)

        document_path = str(tests_path.joinpath('Test.FCStd'))
        self.assertIn(document_path, root_by_document_path)

        root = root_by_document_path[document_path]
        self.assertIsInstance(root, Element)
        self.assertEqual(root.tag, 'Document')
        self.assertEqual(root.attrib['SchemaVersion'], '4')
        self.assertEqual(root.find('Properties').attrib['Count'], '15')


if __name__ == '__main__':
    unittest.main()
