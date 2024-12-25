import re
from pathlib import Path
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from .find_references_in_root import find_references_in_root
from .query import Query
from .reference import Reference

__all__ = ['make_find']


def make_find(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    def find(base_path: str, query: Query) -> List[Reference]:
        references = []
        root_by_document_path = find_root_by_document_path(base_path)
        for document_path, root in root_by_document_path.items():
            document_name = Path(document_path).stem
            # Look for relative references
            # if document_name == query.document:
            #     print(f'Looking for {query._to_string()} in local document ' + query.document)
            #     relative_property_pattern = re.compile(query.property_name)
            #     text_references_in_document = find_references_in_root(document_path, root, relative_property_pattern)
            #     print(text_references_in_document)
            #     references.extend(text_references_in_document)
            #
            #
            #     # relative_property_pattern = re.compile(f'{query.object_name}\\.{query.property_name}')
            #     # text_references_in_document = find_references_in_root(document_path, root, relative_property_pattern)
            #     # references.extend(text_references_in_document)
            # else:
            query_pattern = re.compile(query.to_regex())
            references_in_document = find_references_in_root(
                document_path, root, query)
            references.extend(references_in_document)
                # if len(references_in_document) and query.property_name:
                #     text_pattern = re.compile(r'\b{}(?<!{})\b'.format(
                #         query.property_name, query.to_regex()))
                #     text_references_in_document = find_references_in_root(
                #         document_path, root, text_pattern)
                #     references.extend(text_references_in_document)
        return references
    return find
