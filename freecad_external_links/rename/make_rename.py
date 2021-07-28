from collections import defaultdict
from copy import deepcopy
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from ..find import Property, Reference, make_find


def make_rename(find_root_by_document_path: Callable[[str], Dict[str, Element]]):
    find = make_find(find_root_by_document_path)

    def rename(base_path: str,
               from_property: Property,
               to_property: Property) -> Dict[str, Element]:
        """
        TODO: Person is responsible for manually renaming the property being referenced to,
            in the owner document.
            This script only changes all the cross-document referencens.
        """
        root_by_document_path = find_root_by_document_path(base_path)
        references = find(base_path, from_property)
        references_by_document_path = group_by_document_path(references)
        return rename_references_in_document_xml(root_by_document_path,
                                                 references_by_document_path,
                                                 to_property)
    return rename


def group_by_document_path(references) -> Dict[str, List[Reference]]:
    references_by_document_path = defaultdict(list)
    for reference in references:
        document_path = reference.document_path
        references_by_document_path[document_path].append(reference)
    return references_by_document_path


def rename_references_in_document_xml(root_by_document_path: Dict[str, Element],
                                      references_by_document_path: Dict[str, List[Reference]],
                                      to_property: Property) -> Dict[str, Element]:
    renamed_root_by_document_path = {}
    for document_path, root in root_by_document_path.items():
        references = references_by_document_path[document_path]
        copy = deepcopy(root)
        renamed_root_by_document_path[document_path] = copy
        for reference in references:
            element_with_reference = copy.find(reference.xpath)
            expression_with_reference = element_with_reference.attrib[reference.reference_attribute]
            renamed = expression_with_reference.replace(
                reference.match, str(to_property))
            element_with_reference.set(reference.reference_attribute, renamed)
    return renamed_root_by_document_path
