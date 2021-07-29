from typing import Dict
from xml.etree.ElementTree import Element


def remove(document: str) -> Dict[str, Element]:
    """
    https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyLinks.cpp#L4473-L4510
    https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/App/PropertyLinks.cpp#L3155-L3249

    EMPTY
    =====
    <Cells Count="2" xlink="1">
        <XLinks count="0">
        </XLinks>
        <Cell address="A1" content="Test" />
        <Cell address="B1" content="5" alias="Test" />
    </Cells>
    <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
        <ExpressionEngine count="0">
        </ExpressionEngine>
    </Property>

    XLINKS
    ======
    <Cells Count="4" xlink="1">
        <XLinks count="1" docs="1">
            <DocMap name="Master" label="Master" index="0"/>
            <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
        </XLinks>
        <Cell address="A1" content="Value" />
        <Cell address="B1" content="=Master#Spreadsheet.Value" alias="Value1" />
        <Cell address="D8" content="Value" />
        <Cell address="E8" content="=&lt;&lt;Master&gt;&gt;#&lt;&lt;Spreadsheet&gt;&gt;.Value" alias="Value2" />
    </Cells>
    <ExpressionEngine count="2" xlink="1">
        <XLinks count="2" docs="2">
            <DocMap name="Master" label="Master" index="1"/>
            <DocMap name="Cube" label="Cube" index="0"/>
            <XLink file="Cube.FCStd" stamp="2021-07-25T20:03:03Z" name="Box"/>
            <XLink file="Master.FCStd" stamp="2021-07-25T18:40:15Z" name="Spreadsheet"/>
        </XLinks>
        <Expression path="Height" expression="Cube#Box.Height"/>
        <Expression path="Radius" expression="Master#Spreadsheet.Value"/>
    </ExpressionEngine>
    """
    pass
