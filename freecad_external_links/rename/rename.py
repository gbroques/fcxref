from typing import Dict
from xml.etree.ElementTree import Element

from ..find import Property


def rename(from_property: Property,
           to_property: Property) -> Dict[str, Element]:
    """
    TODO: 1) Find from document
             If not label (not surrounded by << >>),
               Find file named 'XXX.FCStd'.
             Else
               Go through every document looking for the one wit the label

          2) Then find object with name or label.

                <Object name="Spreadsheet">
                    <Properties Count="7" TransientCount="0">
                    <Property name="Label" type="App::PropertyString" status="134217728">
                        <String value="Spreadsheet"/>
                    </Property>

          3) Then find cell with alias.

                <Property name="cells" type="Spreadsheet::PropertySheet" status="67108864">
                    <Cells Count="2" xlink="1">
                        <XLinks count="0">
                        </XLinks>
                        <Cell address="A1" content="Test" />
                        <Cell address="B1" content="5" alias="Test" />
                    </Cells>
                </Property>

          4) Output new XML depending upon to_reference (change alias, spreadsheet name or label).
    """
    pass
