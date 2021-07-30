import time
from glob import glob
from pathlib import Path
from typing import Dict, List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

__all__ = ['find_root_by_document_path', 'write_root_by_document_path']


def find_root_by_document_path(base_path: str, document_pattern: str = '*') -> Dict[str, Element]:
    """Returns a dictionary where keys are document filepaths,
    and values are document xml root elements.
    """
    document_paths = find_document_paths(base_path, document_pattern)
    return _parse_document_xmls(document_paths)


def find_document_paths(base_path: str, document_pattern: str) -> List[str]:
    document_filename = '{}.FCStd'.format(document_pattern)
    pattern = Path(base_path).joinpath('**', document_filename).as_posix()
    return glob(pattern, recursive=True)


def write_root_by_document_path(root_by_document_path: Dict[str, Element]) -> None:
    for document_path, root in root_by_document_path.items():
        with ZipFile(document_path, 'w', ZIP_DEFLATED) as fcstd:
            member = ZipInfo('Document.xml', time.localtime()[:6])
            member.compress_type = ZIP_DEFLATED
            fcstd.writestr(member, ElementTree.tostring(root))


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
