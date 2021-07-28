from glob import glob
from pathlib import Path
from typing import Dict, List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZipFile

__all__ = ['find_root_by_document_path']


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    """Returns a dictionary where keys are document filepaths,
    and values are document xml root elements.
    """
    pattern = Path(base_path).joinpath('**', '*.FCStd').as_posix()
    document_paths = glob(pattern, recursive=True)
    return _parse_document_xmls(document_paths)


def _parse_document_xmls(document_paths: List[str]) -> Dict[str, Element]:
    root_by_document_path = {}
    for document_path in document_paths:
        root = _parse_document_xml(document_path)
        root_by_document_path[document_path] = root
    return root_by_document_path


def _parse_document_xml(document_path: str) -> Element:
    archive = ZipFile(document_path, 'r')
    document_xml = archive.read('Document.xml')
    return ElementTree.fromstring(document_xml)
