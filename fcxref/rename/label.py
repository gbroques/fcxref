import re

__all__ = ['is_label', 'extract_label']


def is_label(object_name: str) -> bool:
    return (
        object_name.startswith('<<') and
        object_name.endswith('>>')
    )


def extract_label(object_name: str) -> str:
    pattern = re.compile('<<(.*)>>')
    match = pattern.match(object_name)
    if not match:
        return object_name
    return match.group(1)
