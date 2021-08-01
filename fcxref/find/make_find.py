import re
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
            property_pattern = re.compile(property.to_regex())
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
