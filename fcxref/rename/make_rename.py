from typing import Callable, Dict, List, Tuple
from xml.etree.ElementTree import Element

from ..find import Property, Reference, make_find
from ..group_references_by_document_path import \
    group_references_by_document_path
from .rename_owner_document import rename_owner_document
from .rename_references_in_root import rename_references_in_root


def make_rename(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    find = make_find(find_root_by_document_path)

    def rename(base_path: str,
               document: str,
               object_name: str,
               from_to_properties: Tuple[str, str]) -> Dict[str, Element]:
        from_property_name, to_property_name = from_to_properties
        root_by_document_path = find_root_by_document_path(base_path)
        from_property = Property(document, object_name, from_property_name)
        to_property = Property(document, object_name, to_property_name)
        references = find(base_path, from_property)
        references_by_document_path = group_references_by_document_path(
            references)
        owner_document_path_by_root = rename_owner_document(
            find_root_by_document_path, base_path, from_property, to_property_name)
        root_by_document_path = rename_references_in_document_xml(root_by_document_path,
                                                                  references_by_document_path,
                                                                  to_property)
        if owner_document_path_by_root:
            root_by_document_path.update(owner_document_path_by_root)
        return root_by_document_path
    return rename


def rename_references_in_document_xml(root_by_document_path: Dict[str, Element],
                                      references_by_document_path: Dict[str, List[Reference]],
                                      to_property: Property) -> Dict[str, Element]:
    renamed_root_by_document_path = {}
    for document_path, references in references_by_document_path.items():
        root = root_by_document_path[document_path]
        copy = rename_references_in_root(root, references, to_property)
        renamed_root_by_document_path[document_path] = copy
    return renamed_root_by_document_path
