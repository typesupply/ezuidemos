"""
Apply string formatting to values in a table.

Relevant Documentation:
- Table: https://typesupply.github.io/ezui/items.html#ezui.Table
- Value Conversion and Formatting: https://typesupply.github.io/ezui/tools.html#value-conversion-and-formatting
"""

import ezui
import random

numbers = list(range(-10, 11))

def colorNumberFormatter(attributes):
    value = attributes["value"]
    if value < 0:
        color = (1, 0, 0, 1)
    elif value > 0:
        color = (0, 1, 0, 1)
    else:
        color = (0, 0, 1, 1)
    attributes["fillColor"] = color


class Demo(ezui.WindowController):

    def build(self):
        content = """
        | --- | @table
        """
        descriptionData = dict(
            table=dict(
                items=[
                    dict(number=random.choice(numbers))
                    for i in range(100)
                ],
                columnDescriptions=[
                    dict(
                        identifier="number",
                        title="Value",
                        editable=True,
                        cellDescription=dict(
                            valueType="integer",
                            stringFormatter=colorNumberFormatter
                        ),
                    ),
                ]
            )
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(100, 200)
        )

    def started(self):
        self.w.open()

    def tableEditCallback(self, sender):
        print("tableEditCallback")


Demo()