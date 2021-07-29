from .find import Property, Reference, make_find
from .rename import make_rename
from .root_by_document_path import find_root_by_document_path

find = make_find(find_root_by_document_path)
rename = make_rename(find_root_by_document_path)

__all__ = ['find', 'rename', 'Property', 'Reference']
