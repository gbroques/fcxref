from pathlib import Path

__all__ = ['extract_document']


def extract_document(document_path: str) -> str:
    return Path(document_path).stem
