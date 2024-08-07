"""
Put simple items into a MerzCollectionView.

Relevant Documentation:

    - MerzCollectionView: https://typesupply.github.io/merz/views/merzCollectionView.html
"""

import ezui
import merz

itemHeight = 100

class DemoController(ezui.WindowController):

    def build(self):
        content = """
        = HorizontalStack

        * TwoColumnForm @settingsForm

        > : Item Count:
        > ---X--- [__] @countSlider

        > : Scale:
        > ---X--- [__] @scaleSlider

        > : Line Height:
        > ---X--- [__] @lineHeightSlider

        > : Spacing:
        > ---X--- [__] @spacingSlider

        > : Alignment:
        > (X) Left @alignmentRadioButtons
        > ( ) Center
        > ( ) Right
        > ( ) Justified

        * MerzCollectionView @merzCollectionView
        """
        descriptionData = dict(
            settingsForm=dict(
                itemColumnWidth=150
            ),
            countSlider=dict(
                valueType="integer",
                value=100,
                minValue=10,
                maxValue=1000,
            ),
            scaleSlider=dict(
                value=0.5,
                minValue=0.25,
                maxValue=2.0,
            ),
            lineHeightSlider=dict(
                minValue=0.5,
                value=1.0,
                maxValue=2.0
            ),
            spacingSlider=dict(
                minValue=-100,
                value=0,
                maxValue=100
            ),
            merzCollectionView=dict(
                delegate=self
            )
        )
        self.w = ezui.EZWindow(
            title="Demo",
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(700, 500),
            minSize=(400, 100),
        )
        self.populateItems()
        self.applySettings()

    def started(self):
        self.w.open()

    def countSliderCallback(self, sender):
        self.populateItems()

    def scaleSliderCallback(self, sender):
        self.applySettings()

    def lineHeightSliderCallback(self, sender):
        self.applySettings()

    def spacingSliderCallback(self, sender):
        self.applySettings()

    def alignmentRadioButtonsCallback(self, sender):
        self.applySettings()

    def applySettings(self):
        collectionView = self.w.getItem("merzCollectionView")
        itemValues = self.w.getItemValues()
        scale = itemValues["scaleSlider"]
        lineHeightFactor = itemValues["lineHeightSlider"]
        lineHeight = itemHeight * lineHeightFactor * scale
        spacing = itemValues["spacingSlider"]
        spacing = spacing * scale
        alignment = itemValues["alignmentRadioButtons"]
        alignment = (
            "left",
            "center",
            "right",
            "justified"
        )[alignment]
        collectionView.setLayoutProperties(
            scale=scale,
            lineHeight=lineHeight,
            spacing=spacing,
            alignment=alignment
        )

    def populateItems(self):
        count = self.w.getItemValue("countSlider")
        count = int(round(count))
        collectionView = self.w.getItem("merzCollectionView")
        existingItems = collectionView.get()
        if len(existingItems) == count:
            return
        widths = [50, 100, 150]
        colors = [(1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5)]
        items = []
        for i in range(count):
            if existingItems:
                item = existingItems.pop(0)
            else:
                item = collectionView.makeItem()
                layer = merz.Oval(
                    position=("center", "center"),
                    size=(25, 25),
                    fillColor=(1, 1, 1, 0.5)
                )
                item.appendLayer("circle", layer)
            width = widths.pop(0)
            color = colors.pop(0)
            widths.append(width)
            colors.append(color)
            with item.propertyGroup():
                item.setHeight(100)
                item.setWidth(width)
                item.setBackgroundColor(color)
                item.setBorderColor((0, 0, 0, 1))
                item.setBorderWidth(1.0)
                item.setCornerRadius(10)
            items.append(item)
        collectionView.set(items)

DemoController()
