import logging
import re
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from .find_references_in_root import find_references_in_root
from .query import Query
from .reference import Reference

__all__ = ['make_find']

logger = logging.getLogger(__name__)

def make_find(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def find(base_path: str, query: Query) -> List[Reference]:
        references = []
        root_by_document_path = find_root_by_document_path(base_path)
        logger.debug(f'Finding references in base path {base_path}')
        for document_path, root in root_by_document_path.items():
            logger.debug(f'Checking document {document_path}')
            query_pattern = re.compile(query.to_regex())
            references_in_document = find_references_in_root(
                document_path, root, query_pattern)
            references.extend(references_in_document)
            if len(references_in_document) and query.property_name:
                text_pattern = re.compile(r'\b{}(?<!{})\b'.format(
                    query.property_name, query.to_regex()))
                text_references_in_document = find_references_in_root(
                    document_path, root, text_pattern)
                references.extend(text_references_in_document)
        return references
    return find
