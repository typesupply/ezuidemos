"""
Make a WindowController that communicates with
multiple glyph editor subscribers.

Relevant Documentation:
    - Subscriber: https://robofont.com/documentation/reference/api/mojo/mojo-subscriber/
"""

import ezui
from mojo.events import postEvent
from mojo.subscriber import (
    Subscriber,
    registerGlyphEditorSubscriber,
    unregisterGlyphEditorSubscriber,
    registerSubscriberEvent
)

demoID = "com.typesupply.demo.ezuiWindowControllingMultipleGlyphEditors"
containerKey = demoID + ".layer"
eventKey = demoID + ".event"

defaultStrokeWidth = 10

class EditorViewDemoUIController(ezui.WindowController):

    def build(self):
        content = """
        --X-- @slider
        """
        descriptionData = dict(
            slider=dict(
                minValue=10,
                maxValue=100,
                value=defaultStrokeWidth
            )
        )
        self.w = ezui.EZPanel(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(200, "auto")
        )

    def started(self):
        self.w.open()
        registerGlyphEditorSubscriber(EditorViewDemo)

    def destroy(self):
        unregisterGlyphEditorSubscriber(EditorViewDemo)

    def sliderCallback(self, sender):
        value = sender.get()
        postEvent(eventKey, strokeWidth=value)


class EditorViewDemo(Subscriber):

    debug = True

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(containerKey)
        self.pathLayer = container.appendPathSublayer(
            strokeColor=(1, 0, 0, 0.5),
            strokeWidth=defaultStrokeWidth
        )

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(containerKey)
        container.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.updateOutline()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.updateOutline()

    def updateOutline(self):
        glyph = self.getGlyphEditor().getGlyph()
        if glyph is None:
            path = None
        else:
            path = glyph.getRepresentation("merz.CGPath")
        self.pathLayer.setPath(path)

    def demoValueChanged(self, info):
        strokeWidth = info["strokeWidth"]
        self.pathLayer.setStrokeWidth(strokeWidth)


def demoInfoExtractor(subscriber, info):
    info["strokeWidth"] = 0
    for lowLevelEvent in info["lowLevelEvents"]:
        info["strokeWidth"] = lowLevelEvent["strokeWidth"]


registerSubscriberEvent(
    subscriberEventName=eventKey,
    methodName="demoValueChanged",
    lowLevelEventNames=[eventKey],
    eventInfoExtractionFunction=demoInfoExtractor,
    dispatcher="roboFont",
    delay=0,
    debug=True
)

OpenWindow(EditorViewDemoUIController)