import re
from pathlib import Path
from re import Pattern
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from .find_references_in_root import find_references_in_root
from .property import Property
from .reference import Reference

__all__ = ['make_find']


def make_find(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def find(base_path: str, property: Property) -> List[Reference]:
        references = []
        root_by_document_path = find_root_by_document_path(base_path)
        for document_path, root in root_by_document_path.items():
            property_pattern = get_property_pattern(document_path, property)
            references_in_document = find_references_in_root(
                document_path, root, property_pattern)
            references.extend(references_in_document)
            if len(references_in_document):
                text_pattern = re.compile(r'\b{}(?<!{})\b'.format(
                    property.property_name, property.to_regex()))
                text_references_in_document = find_references_in_root(
                    document_path, root, text_pattern)
                references.extend(text_references_in_document)
        return references
    return find


def get_property_pattern(document_path: str, property: Property) -> Pattern:
    document_name = get_document_name_from_path(document_path)
    pattern_without_document = '{}\.{}'.format(
        property.object_name,
        property.property_name)
    pattern = property.to_regex() \
        if document_name != property.document \
        else pattern_without_document
    return re.compile(pattern)


def get_document_name_from_path(document_path: str) -> str:
    return Path(document_path).stem
