from .find import Property, Reference, make_find
from .group_references_by_document_path import \
    group_references_by_document_path
from .rename import make_rename
from .root_by_document_path import find_root_by_document_path

find = make_find(find_root_by_document_path)
rename = make_rename(find_root_by_document_path)

__all__ = [
    'find',
    'group_references_by_document_path',
    'rename',
    'Property',
    'Reference'
]
