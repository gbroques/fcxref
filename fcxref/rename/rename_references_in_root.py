import re
from copy import deepcopy
from typing import Dict, List
from xml.etree.ElementTree import Element

from ..find import Property, Reference

__all__ = ['rename_references_in_root']


def rename_references_in_root(root: Dict[str, Element],
                              references: List[Reference],
                              to_property: Property) -> Element:
    copy = deepcopy(root)
    for reference in references:
        element_with_reference = copy.find(reference.xpath)
        expression_with_reference = element_with_reference.attrib[reference.reference_attribute]
        replace_with = str(to_property) if is_fully_qualified_reference(
            reference.match) else to_property.property_name
        renamed = expression_with_reference.replace(
            reference.match, replace_with)
        element_with_reference.set(reference.reference_attribute, renamed)
    return copy


def is_fully_qualified_reference(string: str) -> bool:
    pattern = re.compile(r'.*#.*\..*')
    match = pattern.search(string)
    return bool(match)
