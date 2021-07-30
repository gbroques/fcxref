def is_label(object_name: str) -> bool:
    return (
        object_name.startswith('<<') and
        object_name.endswith('>>')
    )
