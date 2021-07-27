import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree.ElementTree import Element

from freecad_external_links.find_root_by_document_path import \
    find_root_by_document_path


class FindRootByDocumentPath(unittest.TestCase):

    @patch('freecad_external_links.find_root_by_document_path.glob')
    def test_find_root_by_document_path(self, glob):
        tests_path = Path(__file__).parent
        glob.return_value = [str(tests_path.joinpath('Test.FCStd'))]

        root_by_document_path = find_root_by_document_path(str(tests_path))

        self.assertEqual(len(root_by_document_path.items()), 1)

        document_path = str(tests_path.joinpath('Test.FCStd'))
        self.assertIn(document_path, root_by_document_path)

        root = root_by_document_path[document_path]
        self.assertIsInstance(root, Element)
        self.assertEqual(root.tag, 'Document')
        self.assertEqual(root.attrib['SchemaVersion'], '4')
        self.assertEqual(root.find('Properties').attrib['Count'], '15')

        glob.assert_called_once()
        glob_pattern = str(tests_path.joinpath('**', '*.FCStd'))
        glob.assert_called_with(glob_pattern, recursive=True)


if __name__ == '__main__':
    unittest.main()
