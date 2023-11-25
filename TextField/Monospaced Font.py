"""
Set the font in a field to the system's monospaced font.

Relevant Documentation:
- TextField.setFont: https://typesupply.github.io/ezui/items.html#ezui.TextField.setFont
- makeFont: https://typesupply.github.io/ezui/tools.html#ezui.makeFont
"""

import ezui

class Demo(ezui.WindowController):

    def build(self):
        content = """
        [_0102030405060708090_] @field
        """
        descriptionData = dict(
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(300, "auto")
        )
        field = self.w.getItem("field")
        field.setFont(
            name="system-monospaced",
            size=30
        )

    def started(self):
        self.w.open()

Demo()