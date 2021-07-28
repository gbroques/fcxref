from typing import Dict
from xml.etree.ElementTree import Element

from ..find import Property


def rename(from_property: Property,
           to_property: Property) -> Dict[str, Element]:
    """
    TODO: Person is responsible for manually renaming the property being referenced to,
          in the owner document.
          This script only changes all the cross-document referencens.
    """
    pass
