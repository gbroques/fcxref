from glob import glob
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZipFile

__all__ = ['find_root_by_document_path']


def find_root_by_document_path(base_path: str) -> Dict[str, Element]:
    """Returns a dictionary where keys are document filepaths,
    and values are document xml root elements.
    """
    root_by_document = {}
    pattern = Path(base_path).joinpath('**', '*.FCStd').as_posix()
    documents = glob(pattern, recursive=True)
    for document in documents:
        root = _parse_document_xml(document)
        root_by_document[document] = root
    return root_by_document


def _parse_document_xml(document: str) -> Element:
    archive = ZipFile(document, 'r')
    document_xml = archive.read('Document.xml')
    return ElementTree.fromstring(document_xml)
