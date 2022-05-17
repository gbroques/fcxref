__all__ = ['Match']


class Match:
    """Represents a match to a cross-document expression."""

    def __init__(self,
                 reference_attribute: str,
                 location: str,
                 matched_text: str,
                 content: str,
                 location_xpath: str) -> None:
        self.reference_attribute = reference_attribute
        self.location = location
        self.matched_text = matched_text
        self.content = content
        self.location_xpath = location_xpath
