from collections import defaultdict
from typing import Dict, List

from .find import Reference

__all__ = ['group_references_by_document_path']


def group_references_by_document_path(references) -> Dict[str, List[Reference]]:
    references_by_document_path = defaultdict(list)
    for reference in references:
        document_path = reference.document_path
        references_by_document_path[document_path].append(reference)
    return references_by_document_path
