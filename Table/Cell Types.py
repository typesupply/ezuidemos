"""
Use complex cell types in a table.

Relevant Documentation:
- Table: https://typesupply.github.io/ezui/items.html#ezui.Table
"""

import ezui

demoItems = [
    dict(
        imageValue=ezui.makeImage(symbolName="gift.fill"),
        textValue="One",
        popUpValue=0,
        sliderValue=0,
        colorValue=(1, 0, 0, 1)
    ),
    dict(
        imageValue=ezui.makeImage(symbolName="trophy.fill"),
        textValue="Two",
        popUpValue=1,
        sliderValue=0.5,
        colorValue=(0, 1, 0, 1)
    ),
    dict(
        imageValue=ezui.makeImage(symbolName="banknote.fill"),
        textValue="Three",
        popUpValue=2,
        sliderValue=1,
        colorValue=(0, 0, 1, 1)
    ),
]

class Demo(ezui.WindowController):

    def build(self):
        content = """
        | ----------------- | @table
        | im | tf | pu | sl |
        | ----------------- |
        """
        descriptionData = dict(
            table=dict(
                items=demoItems,
                columnDescriptions=[
                    dict(
                        identifier="imageValue",
                        title="Image",
                        width=50,
                        editable=False,
                        cellDescription=dict(
                            cellType="Image"
                        )
                    ),
                    dict(
                        identifier="textValue",
                        title="Text",
                        width=100,
                        editable=True
                    ),
                    dict(
                        identifier="popUpValue",
                        title="PopUp",
                        width=50,
                        editable=True,
                        cellDescription=dict(
                            cellType="PopUpButton",
                            cellClassArguments=dict(
                                items=["A", "B", "C"]
                            )
                        )
                    ),
                    dict(
                        identifier="sliderValue",
                        title="Slider",
                        width=50,
                        editable=True,
                        cellDescription=dict(
                            cellType="Slider",
                            cellClassArguments=dict(
                                minValue=0,
                                maxValue=1
                            )
                        )
                    ),
                    dict(
                        identifier="colorValue",
                        title="Color",
                        width=50,
                        editable=True,
                        cellDescription=dict(
                            cellType="ColorWell"
                        )
                    ),
                ]
            )
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(500, 200)
        )

    def started(self):
        self.w.open()

    def tableEditCallback(self, sender):
        print("tableEditCallback")

Demo()