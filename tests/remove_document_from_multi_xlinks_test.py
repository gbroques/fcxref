import unittest
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from fcxref.remove.remove_document_from_xlinks import \
    remove_document_from_multi_xlinks


class RemoveDocumentFromMultiXLinks(unittest.TestCase):

    def test_remove_document_from_xlinks(self):
        xlinks_element = ElementTree.fromstring("""
            <XLinks count="2" docs="2">
                <DocMap name="Master" label="Master" index="1"/>
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
                <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
            </XLinks>""")
        actual = remove_document_from_multi_xlinks(xlinks_element, 'Master')

        expected = ElementTree.fromstring("""
            <XLinks count="1" docs="1">
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
                </XLinks>""")
        self.assertListEqual(
            ElementTree.tostringlist(actual),
            ElementTree.tostringlist(expected)
        )

    def test_remove_document_from_xlinks_when_doc_map_has_index_zero(self):
        xlinks_element = ElementTree.fromstring("""
            <XLinks count="2" docs="2">
                <DocMap name="Master" label="Master" index="0"/>
                <DocMap name="Cube" label="Cube" index="1"/>
                <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
            </XLinks>""")

        actual = remove_document_from_multi_xlinks(xlinks_element, 'Master')

        expected = ElementTree.fromstring("""
            <XLinks count="1" docs="1">
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
            </XLinks>""")
        self.assertListEqual(
            ElementTree.tostringlist(actual),
            ElementTree.tostringlist(expected)
        )

    def test_remove_document_from_xlinks_when_document_has_multiple_xlinks(self):
        xlinks_element = ElementTree.fromstring("""
            <XLinks count="5" docs="2">
                <DocMap name="Master" label="Master" index="0"/>
                <DocMap name="Cube" label="Cube" index="3"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet1"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet2"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet3"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box1"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box2"/>
            </XLinks>""")

        actual = remove_document_from_multi_xlinks(xlinks_element, 'Master')

        expected = ElementTree.fromstring("""
            <XLinks count="2" docs="1">
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box1"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box2"/>
            </XLinks>""")
        self.assertListEqual(
            ElementTree.tostringlist(actual),
            ElementTree.tostringlist(expected)
        )

    def test_remove_document_from_xlinks_when_document_has_multiple_xlinks_and_xlinks_are_last(self):
        xlinks_element = ElementTree.fromstring("""
            <XLinks count="5" docs="2">
                <DocMap name="Master" label="Master" index="2"/>
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box1"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box2"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet1"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet2"/>
                <XLink file="Master.FCStd" stamp="2021-08-01T19:31:06Z" name="Spreadsheet3"/>
            </XLinks>""")

        actual = remove_document_from_multi_xlinks(xlinks_element, 'Master')

        expected = ElementTree.fromstring("""
            <XLinks count="2" docs="1">
                <DocMap name="Cube" label="Cube" index="0"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box1"/>
                <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box2"/>
                </XLinks>""")
        self.assertListEqual(
            ElementTree.tostringlist(actual),
            ElementTree.tostringlist(expected)
        )


if __name__ == '__main__':
    unittest.main()
