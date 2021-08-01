import logging
import re
from typing import Callable, Dict, Optional, Tuple
from xml.etree.ElementTree import Element

from ..find import Property
from ..find.find_references_in_root import find_references_in_root
from ..rename.rename_references_in_root import rename_references_in_root
from .label import extract_label, is_label

logger = logging.getLogger(__name__)


def rename_owner_document(find_root_by_document_path: Callable[[str, str], Dict[str, Element]],
                          base_path: str,
                          from_property: Property,
                          to_property_name: str) -> Dict[str, Element]:
    document = from_property.document
    find_root = find_document_by_label if is_label(
        document) else find_document_by_name
    document_path_root_pair = find_root(
        find_root_by_document_path, base_path, document)
    if document_path_root_pair is None:
        return None
    document_path, root = document_path_root_pair

    object_name = from_property.object_name
    object_element = find_object_element(root, object_name)
    property_xpath = "Properties/Property[@name='{}']".format('cells')
    cell_xpath = "Cells/Cell[@alias='{}']".format(
        from_property.property_name)
    alias_xpath = join_xpath_expressions(property_xpath, cell_xpath)
    cell_element = object_element.find(alias_xpath)
    if cell_element is not None:
        cell_element.set('alias', to_property_name)
        pattern = re.compile(r'\b{}\b'.format(from_property.property_name))
        references = find_references_in_root(document_path, root, pattern)
        to_property = Property(from_property.document,
                               from_property.object_name,
                               to_property_name)
        copy = rename_references_in_root(root, references, to_property)
        return {document_path: copy}
    return {}


def find_object_element(root: Element, object_name: str) -> Element:
    object_xpath_template = "ObjectData/Object/Properties/Property[@name='Label']*/[@value='{}']/../../.." \
        if is_label(object_name) else "ObjectData/Object[@name='{}']"
    object_xpath = object_xpath_template.format(extract_label(object_name))
    object_element = root.find(object_xpath)
    return object_element


def join_xpath_expressions(*args) -> str:
    return '/'.join(args)


def find_document_by_label(find_root_by_document_path: Callable[[str, str], Dict[str, Element]],
                           base_path: str,
                           document_label: str) -> Optional[Tuple[str, Element]]:
    root_by_document_path = find_root_by_document_path(base_path, '*')
    for document_path, root in root_by_document_path.items():
        xpath = "Properties/Property[@name='Label']*/[@value='{}']".format(
            extract_label(document_label))
        string_element = root.find(xpath)
        if string_element is not None:
            return document_path, root
    return None


def find_document_by_name(find_root_by_document_path, base_path, document_name: str) -> Optional[Tuple[str, Element]]:
    wrapped = with_find_first_logging(find_root_by_document_path)
    root_by_document_path = wrapped(base_path, document_name.replace('_', ' '))
    items = list(root_by_document_path.items())
    return None if len(items) == 0 else items[0]


def with_find_first_logging(find_root_by_document_path: Callable[[str, str], Dict[str, Element]]) -> Callable[[str, str], Dict[str, Element]]:
    def wrapped(base_path, document_pattern):
        root_by_document_path = find_root_by_document_path(
            base_path, document_pattern)
        num_documents = len(root_by_document_path)
        if num_documents == 0:
            logger.info('No document named "{}" found.'.format(
                document_pattern))
            return {}
        elif num_documents > 1:
            first = list(root_by_document_path.keys())[0]
            logger.warn('More than one document named "{}" found. Picking first:\n  {}'.format(
                document_pattern, first))
        return root_by_document_path
    return wrapped
