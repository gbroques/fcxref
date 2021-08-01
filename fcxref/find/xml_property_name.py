from enum import Enum, unique

__all__ = ['XMLPropertyName']


@unique
class XMLPropertyName(Enum):
    """Enumerates XML property names with potential cross-document references.

    XML Examples::

        <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
            ...
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            ...
        </Property>

    See `Core Changes: Link Properties <https://github.com/realthunder/FreeCAD_assembly3/wiki/Core-Changes#link-properties>`_:

        A new class PropertyXLinkContainer is added to support more complex external link usage,
        such as PropertyExpressionEngine and Spreadsheet::PropertySheet.

    """
    cells = 'cells'
    ExpressionEngine = 'ExpressionEngine'
