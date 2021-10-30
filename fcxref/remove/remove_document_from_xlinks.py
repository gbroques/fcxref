from copy import deepcopy
from typing import List
from xml.etree.ElementTree import Element


def remove_document_from_multi_xlinks(xlinks_element: Element,
                                      document_name: str) -> Element:
    """
    Removes document references from XLinks
    when the XLinks element has a count greater than 1.
    """
    copy = deepcopy(xlinks_element)
    matching_doc_map_element = copy.find(f"./DocMap[@name='{document_name}']")
    matching_doc_map_index = int(matching_doc_map_element.attrib['index'])

    all_xlink_elements = copy.findall('XLink')
    all_doc_map_elements = copy.findall('DocMap')
    doc_map_indices = get_sorted_doc_map_indices(all_doc_map_elements)
    next_doc_map_index = doc_map_indices.index(matching_doc_map_index) + 1

    # Remove XLink elements
    if next_doc_map_index < len(doc_map_indices):
        next_index = doc_map_indices[next_doc_map_index]
        for i in range(matching_doc_map_index, next_index):
            copy.remove(all_xlink_elements[i])
    else:
        for i in range(matching_doc_map_index, len(all_xlink_elements)):
            copy.remove(all_xlink_elements[i])

    # Remove matching DocMap element
    copy.remove(matching_doc_map_element)

    # Re-index any DocMap elements left over
    xlink_elements_after_removal = copy.findall('XLink')
    doc_map_elements_after_removal = copy.findall('DocMap')
    for doc_map_element in doc_map_elements_after_removal:
        matching_doc_map_index = int(doc_map_element.attrib['index'])
        xlink_element = all_xlink_elements[matching_doc_map_index]
        new_index = xlink_elements_after_removal.index(xlink_element)
        doc_map_element.attrib['index'] = str(new_index)

    # Update counts on XLinks element
    copy.attrib['count'] = str(len(xlink_elements_after_removal))
    copy.attrib['docs'] = str(len(doc_map_elements_after_removal))

    return copy


def get_sorted_doc_map_indices(doc_map_elements) -> List[int]:
    doc_map_indices = list(
        map(lambda d: int(d.attrib['index']), doc_map_elements))
    doc_map_indices.sort()
    return doc_map_indices
