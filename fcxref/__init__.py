from .find import Query, Reference, make_find
from .group_references_by_document_path import \
    group_references_by_document_path
from .remove import make_remove
from .rename import make_rename_property
from .root_by_document_path import find_root_by_document_path

find = make_find(find_root_by_document_path)
rename_property = make_rename_property(find_root_by_document_path)
remove = make_remove(find_root_by_document_path)

__all__ = [
    'find',
    'group_references_by_document_path',
    'rename_property',
    'remove',
    'Query',
    'Reference'
]
