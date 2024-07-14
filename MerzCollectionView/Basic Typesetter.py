"""
A very basic, unoptimized typesetter.

Relevant Documentation:

    - MerzCollectionView: https://typesupply.github.io/merz/views/merzCollectionView.html
    - Subscriber: https://robofont.com/documentation/reference/api/mojo/mojo-subscriber/
"""

import ezui
import merz
from mojo.UI import splitText
from mojo.subscriber import Subscriber

class DemoController(Subscriber, ezui.WindowController):

    def build(self):
        self.font = CurrentFont()

        content = """
        * HorizontalStack       @controlsStack
        > * GlyphSequence       @textField
        > [__](±)               @pointSizeField
        > [__](±)               @lineHeightField
        > ( {text.alignleft} | {text.aligncenter} | {text.alignright} ) @alignmentSegmentButton
        > (( {circle.fill} | {circle} | {circle.hexagonpath} )) @displaySettingsButton

        * MerzCollectionView    @collectionView
        """
        numberFieldWidth = 40
        descriptionData = dict(
            textField=dict(
                width="fill",
                font=self.font
            ),
            pointSizeField=dict(
                textFieldWidth=numberFieldWidth,
                minValue=20,
                value=150,
                maxValue=500,
                valueIncrement=10,
            ),
            lineHeightField=dict(
                textFieldWidth=numberFieldWidth,
                valueType="float",
                minValue=0.5,
                value=1.0,
                maxValue=2.0,
                valueIncrement=0.1
            ),
            alignmentSegmentButton=dict(
                selected=0
            ),
            displaySettingsButton=dict(
                selected=[0]
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
            minSize=(400, 200),
        )
        self.w.setItemValue("textField", "ABC xyz 123")
        self.controlsStackCallback(None)
        self.displaySettingsButtonCallback(None)
        self.textFieldCallback(None)

    def started(self):
        self.w.open()

    def controlsStackCallback(self, sender):
        collectionView = self.w.getItem("collectionView")
        values = self.w.getItemValues()
        pointSize = values["pointSizeField"]
        lineHeight = values["lineHeightField"]
        alignment = ("left", "center", "right")[values["alignmentSegmentButton"]]
        scale = pointSize / self.font.info.unitsPerEm
        lineHeight = self.font.info.unitsPerEm * lineHeight * scale
        collectionView.setLayoutProperties(
            scale=scale,
            lineHeight=lineHeight,
            alignment=alignment
        )

    def textFieldCallback(self, sender):
        self.unsubscribeFromGlyphs()
        self.glyphNames = self.w.getItemValue("textField")
        font = self.font
        self.glyphs = [font[glyphName] for glyphName in self.glyphNames]
        self.subscribeToGlyphs()
        self.populateItems()

    def displaySettingsButtonCallback(self, sender):
        values = self.w.getItemValue("displaySettingsButton")
        self.showFill = 0 in values
        self.showStroke = 1 in values
        self.showPoints = 2 in values
        items = self.w.getItemValue("collectionView")
        for item in items:
            glyphContainer = item.getLayer("glyphContainer")
            glyphFillLayer = glyphContainer.getSublayer("glyphFill")
            glyphFillLayer.setVisible(self.showFill)
            glyphStrokeLayer = glyphContainer.getSublayer("glyphStroke")
            glyphStrokeLayer.setVisible(self.showStroke)
            glyphPointsLayer = glyphContainer.getSublayer("glyphPoints")
            glyphPointsLayer.setVisible(self.showPoints)

    def populateItems(self):
        collectionView = self.w.getItem("collectionView")
        font = self.font
        glyphs = self.glyphs
        existingItems = collectionView.get()
        items = []
        for glyphName in self.glyphNames:
            if existingItems:
                item = existingItems.pop(0)
            else:
                item = collectionView.makeItem()
                item.getCALayer().setGeometryFlipped_(True) # XXX Ugh. Yell at Tal about this.
                glyphContainer = merz.Base()
                item.appendLayer("glyphContainer", glyphContainer)
                glyphContainer.appendPathSublayer(
                    name="glyphFill",
                    fillColor=(0, 0, 0, 1),
                    visible=True
                )
                glyphContainer.appendPathSublayer(
                    name="glyphStroke",
                    fillColor=None,
                    strokeColor=(1, 0, 0, 1),
                    strokeWidth=1,
                    visible=True
                )
                glyphContainer.appendBaseSublayer(
                    name="glyphPoints",
                    visible=True
                )
            glyph = font[glyphName]
            with item.propertyGroup():
                item.setWidth(glyph.width)
                item.setHeight(font.info.unitsPerEm)
                glyphContainer = item.getLayer("glyphContainer")
                glyphContainer.addTranslationTransformation(
                    value=(0, -font.info.descender),
                    name="descender"
                )
                glyphFillLayer = glyphContainer.getSublayer("glyphFill")
                with glyphFillLayer.propertyGroup():
                    glyphFillLayer.setPath(glyph.getRepresentation("merz.CGPath"))
                    glyphFillLayer.setVisible(self.showFill)
                glyphStrokeLayer = glyphContainer.getSublayer("glyphStroke")
                with glyphStrokeLayer.propertyGroup():
                    glyphStrokeLayer.setPath(glyph.getRepresentation("merz.CGPath"))
                    glyphStrokeLayer.setVisible(self.showStroke)
                glyphPointsLayer = glyphContainer.getSublayer("glyphPoints")
                glyphPointsLayer.clearSublayers()
                with glyphPointsLayer.propertyGroup():
                    for contour in glyph.contours:
                        for point in contour.points:
                            if point.type == "offcurve":
                                imageSettings = dict(
                                    name="oval",
                                    size=(5, 5),
                                    fillColor=None,
                                    strokeColor=(0, 1, 0, 1),
                                    strokeWidth=1
                                )
                            elif point.type == "curve":
                                imageSettings = dict(
                                    name="oval",
                                    size=(10, 10),
                                    fillColor=(0, 1, 0, 1)
                                )
                            elif point.type == "qcurve":
                                imageSettings = dict(
                                    name="star",
                                    size=(12, 12),
                                    fillColor=(0, 1, 0, 1),
                                    pointCount=8,
                                    inner=0.2,
                                    # outer=1.0
                                )
                            else:
                                # line, move
                                imageSettings = dict(
                                    name="rectangle",
                                    size=(8, 8),
                                    fillColor=(0, 1, 0, 1)
                                )
                            x = point.x
                            y = point.y
                            glyphPointsLayer.appendSymbolSublayer(
                                position=(x, y),
                                imageSettings=imageSettings
                            )
                    glyphPointsLayer.setVisible(self.showPoints)
            items.append(item)
        collectionView.set(items)

    def subscribeToGlyphs(self):
        self.setAdjunctObjectsToObserve(set(self.glyphs))

    def unsubscribeFromGlyphs(self):
        self.clearObservedAdjunctObjects()

    def adjunctGlyphDidChangeMetrics(self, info):
        self.populateItems()

    def adjunctGlyphDidChangeOutline(self, info):
        self.populateItems()

DemoController()
